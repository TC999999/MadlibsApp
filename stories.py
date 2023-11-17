"""Madlibs Stories."""
from flask import Flask, request, render_template

# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# app.config["SECRET_KEY"] = "chickensrnice9378467238"

# toolbar = DebugToolbarExtension(app)


class Story:
    """Madlibs story.

    To  make a story, pass a list of prompts, and the text
    of the template.

        >>> s = Story(["noun", "verb"],
        ...     "I love to {verb} a good {noun}.")

    To generate text from a story, pass in a dictionary-like thing
    of {prompt: answer, promp:answer):

        >>> ans = {"verb": "eat", "noun": "mango"}
        >>> s.generate(ans)
        'I love to eat a good mango.'
    """

    def __init__(self, words, text):
        """Create story with words and template text."""

        self.prompts = words
        self.template = text

    def generate(self, answers):
        """Substitute answers into text."""

        text = self.template

        for key, val in answers.items():
            text = text.replace("{" + key + "}", val)

        return text


# Here's a story to get you started


story1 = Story(
    ["place", "noun", "verb", "adjective", "plural_noun"],
    """Once upon a time in a long-ago {place}, there lived a
       large {adjective} {noun}. It loved to {verb} {plural_noun}.""",
)

story2 = Story(
    [
        "plural_animal",
        "verb",
        "plural_noun",
        "second_plural_noun",
        "third_plural_noun",
        "adjective",
    ],
    """There was a group of {plural_animal} who wanted to {verb}. To prepare, they gathered some
    {plural_noun}, then some {second_plural_noun}, and finally some {third_plural_noun}.
    They were so {adjective}, they forgot to start their activity and went back home.""",
)

story3 = Story(
    [
        "country",
        "animal",
        "verb_that_ends_with_ing",
        "second_verb_that_ends_with_ing",
        "food",
        "second_food",
        "number",
        "second_animal",
    ],
    """In the country of {country}, there lived a man who though he was a {animal}. As a result, he would
    spend all day {verb_that_ends_with_ing} and {second_verb_that_ends_with_ing}. The doctor prescribed him with
    a diet of {food} and {second_food} for {number} days. Unfortunately, he instead began thinking that he was
    a {second_animal}.""",
)

all_stories = {"1": story1, "2": story2, "3": story3}


@app.route("/")
def home_page():
    return render_template("home.html")


@app.route("/prompts/<story_num>")
def prompt_page(story_num):
    num = story_num
    new_prompts = all_stories[story_num].prompts
    return render_template("prompts.html", prompts=new_prompts, n=num)


@app.route("/story/<story_num>")
def madlib_story(story_num):
    ans = {}
    story = all_stories[story_num]
    for thing in list(request.args):
        ans[thing] = request.args[thing]
    new_story = story.generate(ans)

    return render_template("story.html", story=new_story)
