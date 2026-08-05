from flask import Flask, render_template
from crud import get_all_tickets

return render_template("index.html")
