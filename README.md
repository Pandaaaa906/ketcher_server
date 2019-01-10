# Ketcher Server
ketcher simple server using flask blueprint.<br>
provides ketcher tools and web service

#### Ketcher v2.0.0-RC+r
A Web-based molecule sketcher<br>
site: https://github.com/epam/ketcher

### How to use

#### In flask script
```python
from flask_ketcher import ketcher

app.register_blueprint(ketcher)

```
#### In template
```html
<iframe id="ketcher-frame" src="{{ url_for('ketcher.editor') }}" scrolling="no"></iframe>
```

#### In javascript
```javascript
var ketcher = $('#ketcher-frame')[0].contentWindow.ketcher
```
### TODO
Fix the chemical recognize function with Imago.