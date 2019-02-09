# Chess Reads, Item Catalog Application

## Intro

The task was to develop an application that provided a list of items within a 
variety of categories as well as provided a user registration and 
authentication system, giving registered users the ability to post, edit and 
delete their own items.

I came up with the catalog of chess books. Non-registered users can access all
the categories and books in the catalog in read-only mode. Registered users 
can add new books to existing categories as well as create own categories.
They can then update and delete only categories they created and books they
added.     

## Implementation of the project

- `db_setup.py` sets up the database and classes >>> *model*;
- `templates` and `static` are responsible for the presentation >>> *view*;
- `app.py` contains main logic of the app >>> *controller*;

## Dependencies (built with) 

- [Python](https://www.python.org/downloads/)
- [Flask](http://flask.pocoo.org/)
- [SQLite](https://www.sqlite.org/index.html)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [oauth2client](https://github.com/googleapis/oauth2client)
- [httplib2](https://github.com/httplib2/httplib2)
- [HTML](https://www.w3.org/html/)
- [CSS](https://www.w3.org/Style/CSS/)
- [JavaScript](https://developer.mozilla.org/bm/docs/Web/JavaScript)
- [jQuery](https://jquery.com/)

## How to run it

 1. Make sure **Python** is installed on your computer. Otherwise, download and 
    install *Python 3.7.2* from the download page (see Dependencies above);
 2. Download and install [Oracle VM Virtual Box](https://www.virtualbox.org/);
    make sure the CPU Virtualization is enabled;
 3. Download and install [Vagrant](https://www.vagrantup.com/);
 4. Download and unzip [VM configuration files](http://bit.ly/2BdmpWt);
 5. You should have the *FSND-Virtual-Machine* directory with the *vagrant* 
    directory inside after the previous step;
 6. [Download](https://github.com/mostrovski/ChessReads/archive/master.zip) and 
    extract this repository so that you have it inside the *vagrant* directory;
 7. In your terminal, `cd` to the *vagrant* directory and run the command 
    `vagrant up` (this causes Vagrant to download the Linux operating system
    and install it. It may take quite a while depending on how fast your
    Internet connection is);
 8. Run `vagrant ssh` command to log into the virtual machine;
 9. Run `cd /vagrant` command to access shared files;
10. `cd` to the app directory (see step 6);
11. Make sure you are on the same level with the `db_setyp.py` file;
12. Run `python db_setup.py` command to setup the database;
13. Run `python db_populate.py` command to populate the database;
14. Run `python app.py` command to start the server;
15. In your browser, open *localhost:8080*; you will need a Google account and
	the Internet connection to log in. 
