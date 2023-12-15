"""
Definition of CLI commands.
"""
import json
import logging
import math
import signal
import sys
from collections import defaultdict
from os import path
from subprocess import check_output
from time import sleep, time
from traceback import format_exc
from typing import DefaultDict, Tuple

import click
import docker
import yaml
from click.types import StringParamType
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

LOGGER = logging.getLogger(__name__)


class AliasedGroup(click.Group):
    """A Click group with short subcommands.

    Example
    -------
    >>> @click.command(cls=AliasedGroup)
    >>> def long_name_command():
    ...     pass
    """

    def get_command(
        self, ctx, cmd_name
    ):  # pylint: disable=inconsistent-return-statements
        cmd = click.Group.get_command(self, ctx, cmd_name)
        if cmd is not None:
            return cmd
        matches = [cmd for cmd in self.list_commands(ctx) if cmd.startswith(cmd_name)]
        if not matches:
            return None
        if len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail("Too many matches: %s" % ", ".join(sorted(matches)))


class StrLength(StringParamType):
    """A Click option type of string with length validation.

    This is basically the same as `str`, except for additional
    functionalities of length validation.

    :param min: Minimum length
    :param max: Maximum length
    :param clamp: Clamp the input if exeeded
    """

    def __init__(
        self, min=None, max=None, clamp=False
    ):  # pylint: disable=redefined-builtin
        self.min = min
        self.max = max
        self.clamp = clamp

    def convert(self, value, param, ctx):
        ret = StringParamType.convert(self, value, param, ctx)
        len_ret = len(ret)
        if self.clamp:
            if self.min is not None and len_ret < self.min:
                return ret + " " * (self.min - len_ret)
            if self.max is not None and len_ret > self.max:
                return ret[: self.max]
        if (
            self.min is not None
            and len_ret < self.min
            or self.max is not None
            and len_ret > self.max
        ):
            if self.min is None:
                self.fail(
                    "Length %d is longer than the maximum valid length %d."
                    % (len_ret, self.max),
                    param,
                    ctx,
                )
            elif self.max is None:
                self.fail(
                    "Length %d is shorter than the minimum valid length %d."
                    % (len_ret, self.min),
                    param,
                    ctx,
                )
            else:
                self.fail(
                    "Length %d is not in the valid range of %d to %d."
                    % (len_ret, self.min, self.max),
                    param,
                    ctx,
                )
        return ret

    def __repr__(self):
        return "StrLength(%d, %d)" % (self.min, self.max)


def to_json_float(value):
    """Convert a float value to a JSON float value.

    :param value: float value
    :return float: JSON float value
    """
    if isinstance(value, list):
        return [to_json_float(v) for v in value]
    if isinstance(value, dict):
        return {k: to_json_float(v) for k, v in value.items()}
    if not isinstance(value, float):
        return value
    if value == math.inf:
        LOGGER.warning("math.inf is converted to sys.float_info.max")
        return sys.float_info.max
    if value == -math.inf:
        LOGGER.warning("-math.inf is converted to -sys.float_info.max")
        return -sys.float_info.max
    if math.isnan(value):
        LOGGER.warning("math.nan is converted to None")
        return None
    return value


def load_config(ctx, self, value):  # pylint:disable=unused-argument
    """Load `ctx.default_map` from a file.

    :param ctx: Click context
    :param self: Self object
    :param value: File name
    :return dict: Loaded config
    """

    if not path.exists(value):
        return {}
    with open(value, encoding="utf-8") as file:
        ctx.default_map = yaml.safe_load(file)
    return ctx.default_map


def save_config(ctx, value):
    """Save `ctx.default_map` to a file.

    :param ctx: Click context
    :param value: File name
    :return dict: Saveed config
    """

    with open(value, "w", encoding="utf-8") as file:
        yaml.dump(ctx.default_map, file)
    return ctx.default_map


def query(ctx, gql_doc, **kwargs):
    """Submit a GraphQL query to a database.

    :param ctx: Click context
    :param gql_doc: str: GraphQL query submitted to a database.
    gql_doc takes either of Q_SOLUTION_TO_EVALUATE, Q_START_EVALUATION, Q_CHECK_BUDGET,
    Q_FINISH_EVALUATION, Q_CANCEL_EVALUATION.
    :param kwargs: GraphQL variables
    :return response: Results returned from a query (gql_doc). response depends on gql_doc.
    For example, when gql_doc=Q_SOLUTION_TO_EVALUATE, response is about a single solution that
    has not been evaluated by objective functions.
    """
    LOGGER.debug("query(%s, %s)", gql_doc, kwargs)
    try:
        response = ctx.obj["client"].execute(gql(gql_doc), variable_values=kwargs)
    except Exception as exc:
        ctx.fail("Exception %s raised when executing query %s\n" % (exc, gql_doc))
    LOGGER.debug("-> %s", response)
    return response


cpu_usages: DefaultDict[Tuple[int, str], float] = defaultdict(float)
"""(match_id, owner_id) -> cpu_usage"""


def wait_to_fetch(ctx, interval):
    """Check if an unevaluated solution exists in a database by calling query every "interval"
    seconds.

    :param ctx: Click context
    :param interval: int: Interval to access a database (second)
    :return solution_id: ID of a solution that has not been evaluated.
    """
    while True:
        response = query(ctx, Q_SOLUTION_TO_EVALUATE)  # Polling
        if response["solutions"]:
            break  # solution found
        sleep(interval)
    LOGGER.debug(cpu_usages)

    # least cpu_usage first
    response["solutions"].sort(
        key=lambda key: cpu_usages[(key["match_id"], key["owner_id"])]
    )
    LOGGER.debug(response["solutions"])
    return response["solutions"][0]["id"]


def check_budget(ctx, user_id, match_id):
    """Check if the budget is exceeded.

    :param ctx: Click context.
    :param user_id: User ID submitting solutions.
    :param match_id: Match ID to submit solutions.
    :raise Exception: When budget exceeded.
    """
    response = query(ctx, Q_CHECK_BUDGET, user_id=user_id, match_id=match_id)
    progress = response["progress"][0]
    n_eval = (
        progress["submitted"] - progress["evaluation_error"] - progress["scoring_error"]
    )
    if n_eval > progress["budget"]:  # Budget exceeded.
        raise Exception("Out of budget: %d / %d." % (n_eval, progress["budget"]))


Q_SOLUTION_TO_EVALUATE = """
query solution_to_evaluate {
  solutions(
    distinct_on: [ match_id, owner_id ]
    order_by: [ { match_id: asc }, { owner_id: asc }, { id: asc }]
    where: { evaluation_started_at: { _is_null: true } }
  ) {
    id
    match_id
    owner_id
  }
}
"""

Q_START_EVALUATION = """
mutation start_evaluation(
  $id: Int!
) {
  update_solutions(
    where: {
      id: { _eq: $id }
      evaluation_started_at: { _is_null: true }
    }
    _set: {
      evaluation_started_at: "now()"
    }
  ) {
    affected_rows
    returning {
      id
      owner_id
      match_id
      match {
        problem { image }
        environments {
          key
          value
        }
      }
      variable
    }
  }
}
"""

Q_CHECK_BUDGET = """
query check_budget(
    $user_id: String!
    $match_id: Int!
) {
  progress(
    limit: 1
    where: {
        user_id: { _eq: $user_id }
        match_id: { _eq: $match_id }
    }
  ) {
    budget
    submitted
    evaluating
    evaluated
    evaluation_error
    scoring
    scored
    scoring_error
  }
}
"""

Q_FINISH_EVALUATION = """
mutation finish_evaluation(
    $id: Int!
    $objective: jsonb
    $constraint: jsonb
    $info: jsonb
    $error: String
) {
  update_solutions_by_pk(
    pk_columns: { id: $id }
    _set: {
      objective: $objective
      constraint: $constraint
      info: $info
      evaluation_error: $error
      evaluation_finished_at: "now()"
    }) {
    id
    updated_at
  }
}
"""

Q_CANCEL_EVALUATION = """
mutation cancel_evaluation(
  $id: Int!
) {
  update_solutions_by_pk(
    pk_columns: { id: $id }
    _set: {
      objective: null
      constraint: null
      info: null
      evaluation_started_at: null
      evaluation_finished_at: null
    }) {
    id
    updated_at
  }
}
"""


def signal_handler(signum, frame):
    raise KeyboardInterrupt


signal.signal(signal.SIGTERM, signal_handler)


@click.command(help="OptHub Evaluator.")
@click.option(
    "-u",
    "--url",
    envvar="OPTHUB_URL",
    type=str,
    default="https://opthub-api.herokuapp.com/v1/graphql",
    help="URL to OptHub.",
)
@click.option(
    "-a", "--apikey", envvar="OPTHUB_APIKEY", type=StrLength(max=64), help="ApiKey."
)
@click.option(
    "-i",
    "--interval",
    envvar="OPTHUB_INTERVAL",
    type=click.IntRange(min=1),
    default=2,
    help="Polling interval.",
)
@click.option(
    "--verify/--no-verify",
    envvar="OPTHUB_VERIFY",
    default=True,
    help="Verify SSL certificate.",
)
@click.option(
    "-r",
    "--retries",
    envvar="OPTHUB_RETRIES",
    type=click.IntRange(min=0),
    default=3,
    help="Retries to establish HTTPS connection.",
)
@click.option(
    "-t",
    "--timeout",
    envvar="OPTHUB_TIMEOUT",
    type=click.IntRange(min=0),
    default=600,
    help="Timeout to process a query.",
)
@click.option(
    "--rm", envvar="OPTHUB_REMOVE", is_flag=True, help="Remove containers after exit."
)
@click.option(
    "-b",
    "--backend",
    envvar="OPTHUB_BACKEND",
    type=click.Choice(["docker", "singularity"]),
    default="docker",
    help="Container backend.",
)
@click.option("-q", "--quiet", count=True, help="Be quieter.")
@click.option("-v", "--verbose", count=True, help="Be more verbose.")
@click.option(
    "-c",
    "--config",
    envvar="OPTHUB_EVALUATOR_CONFIG",
    type=click.Path(dir_okay=False),
    default="opthub-evaluator.yml",
    is_eager=True,
    callback=load_config,
    help="Configuration file.",
)
@click.version_option()
@click.argument("command", envvar="OPTHUB_COMMAND", type=str, nargs=-1)
@click.pass_context
def run(ctx, **kwargs):
    """The entrypoint of CLI.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    if kwargs["backend"] == "docker":
        run_docker(ctx, **kwargs)
    elif kwargs["backend"] == "singularity":
        run_singularity(ctx, **kwargs)
    else:
        raise ValueError(f'Illeagal backend: {kwargs["backend"]}')


def parse_stdout(stdout: str):
    lines = stdout.split("\n")
    lines.reverse()
    for line in lines:
        if line:
            return json.loads(line)


def run_docker(ctx, **kwargs):
    verbosity = 10 * (kwargs["quiet"] - kwargs["verbose"])
    log_level = logging.WARNING + verbosity
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s",
    )
    LOGGER.info("Log level is set to %d", log_level)
    LOGGER.debug("run(%s)", kwargs)
    transport = RequestsHTTPTransport(
        url=kwargs["url"],
        verify=kwargs["verify"],
        retries=kwargs["retries"],
        headers={"X-Hasura-Admin-Secret": kwargs["apikey"]},
    )
    ctx.obj = {
        "client": Client(
            transport=transport,
            fetch_schema_from_transport=True,
        )
    }

    LOGGER.info("Connect to docker daemon...")
    client = docker.from_env()
    LOGGER.info("...Connected")

    n_solution = 1
    LOGGER.info("==================== Solution: %d ====================", n_solution)
    while True:
        try:
            LOGGER.info("Find solution to evaluate...")
            solution_id = wait_to_fetch(ctx, kwargs["interval"])
            LOGGER.debug(solution_id)
            LOGGER.info("...Found")
        except KeyboardInterrupt:
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            LOGGER.warning(format_exc())
            LOGGER.warning("Attempt graceful shutdown...")
            LOGGER.warning("No need to rollback")
            LOGGER.warning("...Shutted down")
            signal.signal(signal.SIGTERM, signal.SIG_DFL)
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            ctx.exit(0)
        except Exception:
            LOGGER.error(format_exc())
            continue

        try:
            LOGGER.info("Try to lock solution to evaluate...")
            response = query(ctx, Q_START_EVALUATION, id=solution_id)
            if response["update_solutions"]["affected_rows"] == 0:
                LOGGER.info("...Already locked")
                continue
            if response["update_solutions"]["affected_rows"] != 1:
                LOGGER.error(
                    "Lock error: affected_rows must be 0 or 1, but %s", response
                )
            solution = response["update_solutions"]["returning"][0]
            LOGGER.info("...Lock aquired")
            start_time = time()

            LOGGER.info("Check budget...")
            check_budget(
                ctx, user_id=solution["owner_id"], match_id=solution["match_id"]
            )
            LOGGER.info("...OK")

            LOGGER.info("Parse variable to evaluate...")
            LOGGER.debug(solution["variable"])
            variable = json.dumps(solution["variable"]) + "\n"
            LOGGER.debug(variable)
            LOGGER.info("...Parsed")

            LOGGER.info("Start container...")
            LOGGER.debug(solution["match"]["problem"]["image"])
            container = client.containers.run(
                image=solution["match"]["problem"]["image"],
                command=kwargs["command"],
                environment={
                    v["key"]: v["value"] for v in solution["match"]["environments"]
                },
                stdin_open=True,
                detach=True,
            )
            LOGGER.info("...Started: %s", container.name)

            LOGGER.info("Send variable...")
            socket = container.attach_socket(
                params={"stdin": 1, "stream": 1, "stdout": 1, "stderr": 1}
            )
            socket._sock.sendall(
                variable.encode("utf-8")
            )  # pylint: disable=protected-access
            LOGGER.info("...Send")

            LOGGER.info("Wait for Evaluation...")
            container.wait(timeout=kwargs["timeout"])
            LOGGER.info("...Evaluated")

            LOGGER.info("Recieve stdout...")
            stdout = container.logs(stdout=True, stderr=False).decode("utf-8")
            LOGGER.debug(stdout)
            LOGGER.info("...Recived")

            if kwargs["rm"]:
                LOGGER.info("Remove container...")
                container.remove()
                LOGGER.info("...Removed")

            LOGGER.info("Parse stdout...")
            out = parse_stdout(stdout)
            LOGGER.debug(out)
            LOGGER.info("...Parsed")

            LOGGER.info("Check budget...")
            check_budget(
                ctx, user_id=solution["owner_id"], match_id=solution["match_id"]
            )
            LOGGER.info("...OK")

            LOGGER.info("Push evaluation...")
            query(
                ctx,
                Q_FINISH_EVALUATION,
                id=solution["id"],
                objective=to_json_float(out.get("objective")),
                constraint=to_json_float(out.get("constraint")),
                info=out.get("info"),
                error=out.get("error"),
            )
            LOGGER.info("...Pushed")
            end_time = time()
            cpu_usages[(solution["match_id"], solution["owner_id"])] += (
                end_time - start_time
            )

        except KeyboardInterrupt:
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            LOGGER.warning(format_exc())
            LOGGER.warning("Attempt graceful shutdown...")
            LOGGER.warning("Rollback evaluation...")
            query(ctx, Q_CANCEL_EVALUATION, id=solution["id"])
            LOGGER.warning("...Rolled back")
            LOGGER.warning("...Shutted down")
            signal.signal(signal.SIGTERM, signal.SIG_DFL)
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            ctx.exit(0)
        except Exception as exc:
            LOGGER.error(format_exc())
            LOGGER.info("Finish evaluation...")
            query(
                ctx,
                Q_FINISH_EVALUATION,
                id=solution["id"],
                objective=None,
                constraint=None,
                info=None,
                error=str(exc),
            )
            LOGGER.info("...Finished")
            continue

        n_solution += 1
        LOGGER.info(
            "==================== Solution: %d ====================", n_solution
        )


def run_singularity(ctx, **kwargs):
    verbosity = 10 * (kwargs["quiet"] - kwargs["verbose"])
    log_level = logging.WARNING + verbosity
    logging.basicConfig(level=log_level)
    LOGGER.info("Log level is set to %d", log_level)
    LOGGER.debug("run(%s)", kwargs)
    transport = RequestsHTTPTransport(
        url=kwargs["url"],
        verify=kwargs["verify"],
        retries=kwargs["retries"],
        headers={"X-Hasura-Admin-Secret": kwargs["apikey"]},
    )
    ctx.obj = {
        "client": Client(
            transport=transport,
            fetch_schema_from_transport=True,
        )
    }

    n_solution = 1
    LOGGER.info("==================== Solution: %d ====================", n_solution)
    while True:
        try:
            LOGGER.info("Find solution to evaluate...")
            solution_id = wait_to_fetch(ctx, kwargs["interval"])
            LOGGER.debug(solution_id)
            LOGGER.info("...Found")
        except KeyboardInterrupt:
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            LOGGER.warning(format_exc())
            LOGGER.warning("Attempt graceful shutdown...")
            LOGGER.warning("No need to rollback")
            LOGGER.warning("...Shutted down")
            signal.signal(signal.SIGTERM, signal.SIG_DFL)
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            ctx.exit(0)
        except Exception:
            LOGGER.error(format_exc())
            continue

        try:
            LOGGER.info("Try to lock solution to evaluate...")
            response = query(ctx, Q_START_EVALUATION, id=solution_id)
            if response["update_solutions"]["affected_rows"] == 0:
                LOGGER.info("...Already locked")
                continue
            if response["update_solutions"]["affected_rows"] != 1:
                LOGGER.error(
                    "Lock error: affected_rows must be 0 or 1, but %s", response
                )
            solution = response["update_solutions"]["returning"][0]
            LOGGER.info("...Lock aquired")
            start_time = time()

            LOGGER.info("Check budget...")
            check_budget(
                ctx, user_id=solution["owner_id"], match_id=solution["match_id"]
            )
            LOGGER.info("...OK")

            LOGGER.info("Parse variable to evaluate...")
            LOGGER.debug(solution["variable"])
            variable = json.dumps(solution["variable"]) + "\n"
            LOGGER.debug(variable)
            LOGGER.info("...Parsed")

            LOGGER.info("Start container...")
            LOGGER.debug(solution["match"]["problem"]["image"])
            LOGGER.info("Evaluate...")
            cmd = (
                "singularity",
                "run",
                "--writable",
                "--env",
                ",".join(
                    f'{v["key"]}={v["value"]}'
                    for v in solution["match"]["environments"]
                ),
                solution["match"]["problem"]["image"],
            ) + kwargs["command"]
            LOGGER.debug(cmd)
            stdout = check_output(
                cmd,
                input=variable,
                text=True,
                timeout=kwargs["timeout"],
            )
            LOGGER.debug(stdout)
            LOGGER.info("...Evaluated")

            LOGGER.info("Parse stdout...")
            out = parse_stdout(stdout)
            LOGGER.debug(out)
            LOGGER.info("...Parsed")

            LOGGER.info("Check budget...")
            check_budget(
                ctx, user_id=solution["owner_id"], match_id=solution["match_id"]
            )
            LOGGER.info("...OK")

            LOGGER.info("Push evaluation...")
            query(
                ctx,
                Q_FINISH_EVALUATION,
                id=solution["id"],
                objective=to_json_float(out.get("objective")),
                constraint=to_json_float(out.get("constraint")),
                info=out.get("info"),
                error=out.get("error"),
            )
            LOGGER.info("...Pushed")
            end_time = time()
            cpu_usages[(solution["match_id"], solution["owner_id"])] += (
                end_time - start_time
            )

        except KeyboardInterrupt:
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            LOGGER.warning(format_exc())
            LOGGER.warning("Attempt graceful shutdown...")
            LOGGER.warning("Rollback evaluation...")
            query(ctx, Q_CANCEL_EVALUATION, id=solution["id"])
            LOGGER.warning("...Rolled back")
            LOGGER.warning("...Shutted down")
            signal.signal(signal.SIGTERM, signal.SIG_DFL)
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            ctx.exit(0)
        except Exception as exc:
            LOGGER.error(format_exc())
            LOGGER.info("Finish evaluation...")
            query(
                ctx,
                Q_FINISH_EVALUATION,
                id=solution["id"],
                objective=None,
                constraint=None,
                info=None,
                error=str(exc),
            )
            LOGGER.info("...Finished")
            continue

        n_solution += 1
        LOGGER.info(
            "==================== Solution: %d ====================", n_solution
        )
