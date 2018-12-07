# Free-Stuff-Exchange
CS50's Final Project (Fall 2018) - A forum for students on Harvard campus to exchange free merch they have

#Free Stuff Exchange Design

We made a couple of design choices that might seem odd at first, but given our skill level these design choices are the best way to make progress and gurantee a finished project in the worst case senerio.

Initally we chose to design the website around finance as it was a practical way to get our project started and make the the website look clean.
We decided that we were going to implement this website on the CS50 IDE, incorporating Flask, Python, Javascript, jinja, html, css, and html.
We chose to keep the login and register parts of the page mostly the same, with the exception of the user name. We made the user enter a valid email as their username as a means to give other users on the website an easy way to contact them. Where ever there is a contact button, we have simply created a button that enters the users username into a email header.
We then decided that we needed a simple and scaleable way to add and search for items in our inventory. We decided to limit the the number of item types to just those that we entered into a table. That way we could search for and compare items without having to worry about slight differences in the naming convention of certian items making it difficult to find things on the website. We also made this a seperate table because we wanted the user to easily be able to select from a dynamic list of items as they registered items and itemtypes that they were looking for. Having the itemtypes in a seperate page also allowed us to change the item type names without much concern as we were passing numbers between databases.
Our match page gives users the ability to look at items that that had a matching item type. After we added a search function on a list of all items registered on the website, it might not seem like it is nessiary to keep match around, however we decided to keep match as it allowed for a useful level of precision when searching for items. Though the search function was very powerful, it would only make sense for the specific item name rather than item type, so it operates on that level of specificity.
For items in the inventory we also added the option to add a description of the item as well as a picture of the item. We wanted the users to be to show unique features of an item on our website, so these seemed like good ways to do that.
