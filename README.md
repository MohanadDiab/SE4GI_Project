# SE4GI_Project
 This repository is dedicated to the project part of the software engineering course
## Structure
| Name       | Description  |
| ---- | ------------ | 
| template | Web page template for Web application  | 
| static | Static documents for Web application  | 
| ml_monitor.py | Continuously running to monitor requests of predict house quality by random forest  | 
| web.py | Flask/Jinja2 style web application  | 
| rf.dat | Model trained by ./preCode/ml_pre.py  | 
| dbConfig.txt | PostgreSQL database connection string in json format | 

## Requirements
Python 3.7+
Package requirements can be found at requirements.txt
## Run the project
Run run.sh on Windows/Linux system
## Preview of this project
http://shengshen.li/

**Website guide for the website Realty:**

This document represents a user guide to navigate through the site, to
allow users to fully use the site as intended by the development team.

**The overall structure of the website:**

There's an extra page that allows the user to enter their profile, not
mentioned in the graph in this version.

![](SE4GI_Project/Documentation/web app guide/vertopal_948326db09924f1e8fc32266397611fc/media/image1.JPG){width="6.0in"
height="6.007638888888889in"}

1.  **The visitors section:**

The visitors section includes pages that allow the visitor to view the
home page of the site, to sign in if they have an account, to sign up if
they don't have an account, and to view some information about the site
through the about us page.

1.  **The home page:**

The home page displays a user friendly user interface to allow the user
to navigate to the sign in screen.

![](/repository/Documentation/web app guide/vertopal_948326db09924f1e8fc32266397611fc/media/image2.jpeg){width="6.0in"
height="3.640972222222222in"}

1.  **The sign in page:**

The sign in page allows the user to sign in using their credentials.

![](vertopal_948326db09924f1e8fc32266397611fc/media/image3.jpeg){width="6.0in"
height="3.640972222222222in"}

2.  **The sign up page:**

The sign up page allows the users to create a new account.

![](vertopal_948326db09924f1e8fc32266397611fc/media/image4.jpeg){width="6.0in"
height="3.7194444444444446in"}

3.  **The about us page:**

This page offers some info about the site and its components/features,
it also allows the user to view the open source data used in the
project.

![](vertopal_948326db09924f1e8fc32266397611fc/media/image5.jpeg){width="3.0833333333333335in"
height="7.620137795275591in"}

1.  **The users section:**

The users section includes pages that allow the users to view the home
page of the site, to view maps, to view graphs, view their profile, and
to view some information about the site through the about us page.

The users section uses a different base template, changes in the header
are seen to account for user of they are in the session or not, if in
any instance of time the user chooses to log out, the visitor's pages
and their respective base template will render again.

1.  **The home page:**

The home page displays a user friendly user interface to allow the user
to navigate to the sign in screen.

![](vertopal_948326db09924f1e8fc32266397611fc/media/image6.jpeg){width="6.0in"
height="3.640972222222222in"}

2.  **The maps page:**

The maps page displays a user friendly user interface to allow the user
to navigate to the maps screen.

![](vertopal_948326db09924f1e8fc32266397611fc/media/image7.jpeg){width="6.0in"
height="5.4118055555555555in"}

3.  **The graphs page:**

The graphs page displays a user friendly user interface to allow the
user to navigate to the graphs screen.

![](vertopal_948326db09924f1e8fc32266397611fc/media/image8.jpeg){width="6.0in"
height="3.001388888888889in"}

4.  **The profile page:**

The profile page displays a user friendly user interface to allow the
user to navigate to their profile screen.

![](vertopal_948326db09924f1e8fc32266397611fc/media/image9.jpeg){width="6.0in"
height="3.1284722222222223in"}

5.  **The about us page:**

The home page displays a user friendly user interface to allow the user
to navigate to the maps screen.

![](vertopal_948326db09924f1e8fc32266397611fc/media/image10.jpeg){width="3.138888888888889in"
height="7.757439851268591in"}

**Extras:**

In this section are extra screens that display a sample of the maps and
the graphs that the users are able to view.

![](vertopal_948326db09924f1e8fc32266397611fc/media/image11.jpeg){width="6.0in"
height="3.5694444444444446in"}

![](vertopal_948326db09924f1e8fc32266397611fc/media/image12.jpeg){width="6.0in"
height="3.5284722222222222in"}
