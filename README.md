# ditto
a personality-based, dynamic NPC dialogue generator.

## Basic Overview
ditto generates realtime dialogue for personality-rich NPC's.

### Roadmap
The biggest issues with ditto right now are in part due to the limitations of GPT-3.5, ditto is built to work with any language model so hopefully when newer and faster/smarter AI are available, ditto will grow with them.
- Increase response speed
- Optimize knowledge compilation

Some features that are being worked at the moment include
- Improve character dialogue customizability (currently no effective way to give a character an accent or set of vernacular)
- simple memory (knowledge created dynamically based on information gained in conversation.)

## Get Started
Clone:

    git clone www.github.com/directiory my_dir

Import as python module:

    import ditto

## Usage
Each ditto project consists of a directory that defines the world, its enviroments, and the characters:

	ditto_world_filetree
	├── characters
	│   └── default_character
	│       ├── personal.know
	│       └── physical.know
	├── enviroments
	│   └── enviroment_name.know
	├── etc
	│   └── misc_info_0.know
	├── condsiderations
	└── world.know

for a character to function it needs at *least* a `personal.know`, this is what gives each character their personality.

### Knowledges
each character is comprised of different "knowledges" (.know files)

 - personal
	 - information on how the character ACTS. This is where the model is informed on the personality of the character
 - physical
	 - information on what the character LOOKS LIKE. This is not neccesary but enables the character to understand and make references made to its apperance. 
 - enviromental
	 - information on the general enviroment surrounding a given character. This enables them to understand and make references to their immediate enviroment
 - global
	 - general information on the world or region they inhabit. This can include global knowledges such as political and moral views, or established social conventions. 
 - etc
	 - any other available knowledges characters should be able to reference, such as the appearances and behaviors of misc. plants and animals, or any other facts.

#### Formatting
Each knowledge can be written in one of two ways:

**Paragraph style:**
[a paragraph description of a character]

**List style:**
[list style description of the same character]

Both styles have their pros and cons and are better suited for different kinds of knowledges.

Use the list format for personal and physical knowledges; as it is much easier to add, remove, or edit a single bullet point entry if a character is behaving weird.

Using the paragraph format for describing enviromental, and global, and etc knowledges allows for more contextual information to be conveyed and is less confusing for human readers. The modularity of these knowledges is less important as they dont contribute directly to the behavior of each character and won't be tinkered with as often.

#### Syntax
`.know` files are stored as plaintext, but are processed with some specific syntax to make writing them easier.

**Comments:**

	;; this is a comment
	This statement is vital information ;; everything over here is a comment (your character will ignore this)

**Imports**

`% import etc/snail_faq.know` (this implies the project directory's `etc`)

`% import ~/directory/to/absolute/file.know` (for absolute paths to `.know` files)

### Actions
Actions give characters abilities to execute code in your program. In the example of a video game, the NPC can choose to perform a "give_item" action if the player asks for some item.

Actions are defined with an identifier, description, optional parameters, and a function to execute when the character decides to use it.

#### Example
This is an action that gives the character the ability to show the player an item.

	Name: "show_item"
	Description: "Shows the player an item, you simply hold it out for them to see. The player does not keep this item"
	Options: "hat, necklace, bracelet, playing_cards"
	Function: show_item_action

where "show_item_action" is defined:

    def show_item_action(item):
	    print("[Showing " +  item + "]")
	    return
Then, when the character feels it is appropriate to execute this action, it will select the most relevent parameter and execute the given function with that parameter.

## Background info
