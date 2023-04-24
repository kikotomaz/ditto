# Ditto
Ditto is a realtime NPC dialogue generator that creates personality-rich characters, breathing a new life into virtual worlds.

## Get Started
Clone:

    git clone https://github.com/kikotomaz/npc-dio my_dir

Import as python module:

    import ditto

## Usage
Each ditto project consists of a directory that defines the world, its enviroments, and the characters:

	ditto_world_filetree
	├── characters
	│   └── default_character
	│       ├── personal.know
	│       ├── physical.know
	│       └── etc.know
	├── enviroments
	│   └── enviroment_name.know
	├── etc
	│   └── misc_info_0.know
	├── condsiderations
	└── world.know

for a character to function it needs at *least* a `personal.know`, this is what gives each character their personality.

### Knowledges
each character is comprised of different "knowledges" (`.know` files)

 - personal
	 - information on how the character ACTS. This is where the character is informed on their personality and backstory
 - physical
	 - information on what the character LOOKS LIKE. This is not neccesary but enables the character to understand and make references made to its apperance.  
 - enviromental
	 - information on the general enviroment surrounding a given character. This enables them to understand and make references to their immediate enviroment
 - world
	 - general information on the world or region they inhabit. This includes more abstract information such as common knowledge that individuals of this world carry, globally accepted values, or the state of the world. Every character in the project will have access to this information. 
 - etc
	 - any other available knowledges characters should be able to reference, such as the appearances and behaviors of misc. plants and animals, or any other facts. These knowledges are only available to a character if it is explicitly imported using an import statement in the header of another accesible knowledge such as `personal.know` or as a parameter during the creation of the character.

#### Syntax
`.know` files are stored as plaintext, but are processed with some specific syntax to make writing them easier.

**Comments:**
Comments in `.know` files work exactly as you would probably expect. They use the `;;` prefix:

	;; this is a comment
	This statement is vital information ;; everything over here is a comment (your character will ignore this)

**Imports**
To avoid rewriting the same knowledge over and over again, you can write it once and reference it in any other knowledge file.
Typically, this is how files in the 'etc/' directory are used, but you can also reference any `.know` file such as a enviroment or the physical descriptions of another character

Syntax:

	% relative/path/to/file.know

For example if you were to add:

	% etc/snail_faq.know

to your `world.know`, every character in your project would be able to have a conversation about snails. If instead you put it in a characters `characters/example_name/etc.know` then only that character would know about snails. 

#### Formatting
Each knowledge can be written in one of two ways:

**Paragraph style:**
[a paragraph description of a character]

**List style:**
[list style description of the same character]

Both styles have their pros and cons and are better suited for different kinds of knowledges.

Use the list format for personal knowledges; as it is much easier to add, remove, or edit a single bullet point entry if a character is behaving weird.

Using the paragraph format for describing enviromental, and global, and etc knowledges allows for more contextual information to be conveyed and is less confusing for the writers writing these knowledges. The modularity of these knowledges is less important as they dont contribute directly to the behavior of each character, and won't be tinkered with as often.

### Actions
Actions are what give characters the ability to execute code in your program. In the example of a video game, the NPC can choose to perform a "give_item" action if the player asks for some item.

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

## Roadmap
The biggest issues with ditto right now are in part due to the limitations of GPT-3.5, ditto is built to work with any language model so hopefully when newer and faster/smarter AI are available, ditto will grow with them.
- Increase response speed
- Optimize knowledge compilation

Some features that are being worked at the moment include
- Improve character dialogue customizability (currently no effective way to give a character an accent or set of vernacular)
- simple memory (knowledge created dynamically based on information gained in conversation.)

## Background info
