# Free-Stuff-Exchange
CS50's Final Project (Fall 2018) - A forum for students on Harvard campus to exchange free merch they have

#Free Stuff Exchange Design

We made a couple of design choices that might seem odd at first, but given our skill level these design choices are the best way to make progress and gurantee a finished project in the worst case senerio.

Initally we chose to design the website around finance as it was a practical way to get our project started and make the the website look clean.
We decided that we were going to implement this website on the CS50 IDE, incorporating Flask, Python, Javascript, jinja, html, css, and html.
We chose to keep the login and register parts of the page mostly the same, with the exception of the user name. We made the user enter a valid email as their username as a means to give other users on the website an easy way to contact them. Where ever there is a contact button, we have simply created a button that enters the users username into a email header.
We then decided that we needed a simple and scaleable way to add and search for items in our inventory. We decided to limit the the number of item types to just those that we entered into a table. That way we could search for and compare items without having to worry about slight differences in the naming convention of certian items making it difficult to find things on the website. We also made this a seperate table because we wanted the user to easily be able to select from a dynamic list of items as they registered items and itemtypes that they were looking for. Having the itemtypes in a seperate page also allowed us to change the item type names without much concern as we were passing numbers between databases.
Our match page gives users the ability to look at items that that had a matching item type. After we added a search function on a list of all items registered on the website, it might not seem like it is nessiary to keep match around, however we decided to keep match as it allowed for a useful level of precision when searching for items. Though the search function was very powerful, it would only make sense for the specific item name rather than item type, so it operat

## Features
- Register
- Homepage
- Add
- Search
- LookForItemType
- Match

###Accounts

####Registering Accounts

Our website allows users to register an account by entering a valid email, and also allows users to login

Register
<img src="/static/Demo_images/Screenshots/Screenshot (1).png" width="85%" >

Valid Entry for Register
<img src="/static/Demo_images/Screenshots/Screenshot (2).png" width="85%" >

Login Page
<img src="/static/Demo_images/Screenshots/Screenshot (16).png" width="85%" >

###Homepage
This is what the homepage looks like:
<img src="/static/Demo_images/Screenshots/Screenshot (15).png" width="85%" >
You can click on My Stuff to get to the Homepage

The homepage lists the items that you own and the itemtypes you are looking for

You can click on delete beside itemtypes and items to delete them from your inventory

###Add items
Going to the add page allows users to add items to their inventory
<img src="/static/Demo_images/Screenshots/Screenshot (15).png" width="85%" >
They need to enter a Item Name, Item Type, Item Description, and Upload an image inorder to register an item

###Search
Going to the search page will give you a search bar that allows you to both see and search through all the items on the website by item name.
<img src="/static/Demo_images/Screenshots/Screenshot (17).png" width="85%" >
From here you can click on contact to send the owner an email to request their item.

###LookForItemType
Going to the LookForItemType will allow you to enter a specific item type that you are looking for, which will be displayed for you on the match page
<img src="/static/Demo_images/Screenshots/Screenshot (14).png" width="85%" >

###Match
Going to the Match page will display all the items of the types that you are looking for.
<img src="/static/Demo_images/Screenshots/Screenshot (18).png" width="85%" >
From here you can click on contact to send the owner an email to request their item.



