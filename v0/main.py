# This script exists only to help trigger preloading
# of pyodide.

from js import console


if __name__ == "__main__":
    console.log("""\
I'm a lumberjack, and I'm okay
I sleep all night and I work all day
I cut down trees, I eat my lunch
I go to the lavatory
On Wednesdays I go shoppin'
And have buttered scones for tea.

I'm a lumberjack, and I'm okay
I sleep all night and I work all day
I cut down trees, I skip and jump
I like to press wild flowers
I put on women's clothing
And hang around in bars.

I'm a lumberjack, and I'm okay
I sleep all night and I work all day
I cut down trees, I wear high heels
Suspendies, and a bra
I wish I'd been a girlie
Just like my dear Papa.\
""")
