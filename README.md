# Ketcher Server
ketcher simple server using flask blueprint.<br>
provides ketcher tools and web service

#### Ketcher v2.0.0-RC+r
A Web-based molecule sketcher<br>
site: https://github.com/epam/ketcher

### How to use

In flask script
```
python
from flask_ketcher import ketcher

app.register_blueprint(ketcher.bp)

```
In template

### TODO
Fix the chemical recognize function with Imago.