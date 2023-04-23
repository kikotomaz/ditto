# ditto
a personality-based, dynamic NPC dialogue generator.

## Basic Overview
ditto generates realtime dialogue for personality-rich NPC's.

## Get Started
Clone:

    git clone www.github.com/directiory my_dir

Import as python module:

    import ditto

## Usage
### Knowledges
each character is comprised of different "knowledges" (.know files)

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
	
 - personal
	 - information on how the character ACTS. This is where the model is informed on the personality of the character
 - physical
	 - information on what the character LOOKS LIKE. This is not neccesary but enables the character to understand and make references made to its apperance. 
 - enviromental
	 - information on the general enviroment surrounding a given character. This enables them to understand and make references to their immediate enviroment
 - global
	 - general information on the world or region they inhabit. This can include global knowledges such as political or philisofical views 
 - etc
	 - any other available knowledges characters should be able to reference, such as the appearances and behaviors of misc. plants and animals, or any other facts.

#### Formatting
Each knowledge can be written in one of two ways:

##### Paragraph style
[a paragraph description of a character]
##### List style
[list style description of the same character]

Both styles have their pros and cons and are better suited for different kinds of knowledges.

Use the list format for personal and physical knowledges; as its much easier to add, remove, or edit a single bullet point if a character is behaving weird.

Using the paragraph format for describing enviromental, and global, and etc knowledges allows for more contextual information to be conveyed and is less confusing. The modularity of these knowledges is less important as they dont contribute directly to the behavior of the character so they won't be tinkered with as much.

### Actions
Actions give characters abilities to execute predefined code in the program. In the example of a video game, the NPC can choose to perform a "give_item" action if the player asks for some item.

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
