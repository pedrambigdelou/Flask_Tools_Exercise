from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# key names will use to store some things in the session;
# put here as constants so we're guaranteed to be consistent in
# our spelling of these
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def show_survey_start():
  """Select a survey."""

  return render_template("survey_start.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
  """Clear the session of responses."""

  session[RESPONSES_KEY] = []

  return redirect("/questions/0")

@app.route("/questions/<int:qid>")
def show_question(qid):
  """Display current question."""
  responses = session.get(RESPONSES_KEY)

  if (responses is None):
    # trying to access question page too soon
    return redirect("/")

  if (len(responses) == len(survey.questions)):
    # They've answered all the questions! Thank them.
    return redirect("/complete")

  if (len(responses) != qid):
    # Trying to access questions out of order.
    flash(f"Invalid question id: {qid}.")
    return redirect(f"/questions/{len(responses)}")

  question = survey.questions[qid]
  return render_template(
    "question.html", question_num=qid, question=question)
