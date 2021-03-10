from random import choice
import textwrap


def print_random_quote():
    quotes = [
        (
            "I feel the best I am going to feel all day when I do Wim Hof. I've never regretted doing it",
            "Steven Massicotte"),
        ("I see open eye visuals when I do the breath hold", "Sebastian Jurga"),
        ("It's so fucking good man", "Aaron Massicotte"),
        ("Wim would be proud :)", "Aaron Massicotte"),

        ("If you can learn how to use your mind, anything is possible.", "Wim Hof, Becoming the Iceman"),
        ("I'm not afraid of dying. I'm afraid not to have lived.", "Wim Hof"),
        (
            "Fear does not go away by itself. You have to confront your fear, mold it, then learn to control it in it's own irrational reality. Every human being has the power to do just that. To go deep within and confront your inner being is a powerful act. Going deep and developing the will power is the only way.",
            "Wim Hof, Becoming the Iceman"),
        (
            "In the Bhagavad Gita they say, \"The mind under control is your best friend, the mind wandering about is your worst enemy.\" Make it your best friend, to the point where you can rely on it. Your mind makes you strong from within. It is your wise companion. The sacrifices you make will be rewarded. Life doesn't change, but your perception does. It's all about what you focus on. Withdraw from the world's influence and no longer be controlled by your emotions. If you can grab the wheel of your mind, you can steer the direction of where your life will go.",
            "Wim Hof, Becoming the Iceman"),
        (
            "There is so much more to life than meets the eye if you choose to seek it. The seeker becomes the finder, the finder of so much more than we thought was possible.",
            "Wim Hof, The Wim Hof Method"),
        ("Through deep breathing we become alchemists", "Wim Hof"),
        ("BREATHE MOTHERFUCKER!!!", "Wim Hof"),
        ("Death is nothing more than a concept...\n\t\t...Breath is the life force!", "Wim Hof"),
        ("The breath knows how to go deeper than the mind", "Wim Hof")
    ]

    chosen_quote, chosen_quoter = choice(quotes)
    print('\n'.join(textwrap.wrap(chosen_quote, 100, replace_whitespace=False)))
    print('\t - ' + chosen_quoter)


if __name__ == "__main__":
    print_random_quote()
