function toggleView(type, id, onoff) {
    view = $(type + '-view-' + id);
    edit = $(type + '-edit-' + id);
    
    if (onoff) {
        set_visible(edit);
        set_invisible(view);
    } else {
        set_visible(view);
        set_invisible(edit);    
    }    
    /*  Add 'Now' and 'Today' buttons to each field via javascript
     *  Django normally does this onload but then it does not change dynamically added fields,
     *  so we're doing this every time user clicks on 'Edit'
     */
    DateTimeShortcuts.init();
}

function set_visible(obj) {
    obj.addClassName('visible');
    obj.removeClassName('invisible');
}

function set_invisible(obj){
    obj.addClassName('invisible');
    obj.removeClassName('visible');
}

function update_metasense() {
    /*new Ajax.Request('http://metalab.at/metasense/status.html', {asynchronous:true, onFailure:function(){}, onException:function(){}, onSuccess:function(transport){ */
    new Ajax.Request('/metasense/status.html', {asynchronous:true, onFailure:function(){}, onException:function(){}, onSuccess:function(transport){ 
        oopen = $('presence_open');
        oclosed = $('presence_closed');
        if(transport.responseText.match("ffnet")) {
            set_visible(oopen);
            set_invisible(oclosed);
          } else if( transport.responseText.match("niemand")){            
            set_visible(oclosed);
            set_invisible(oopen);            
        } else {
            set_invisible(oopen);
            set_invisible(oclosed);
        }
    }});
}

function do_on_load()
{
    update_metasense();
    DateTimeShortcuts.init();
}

function enter_pressed(e){
    var keycode;
    if (window.event) keycode = window.event.keyCode; 
    else if (e) keycode = e.which; 
    else return false; 
    return (keycode == 13); 
}

addEvent(window, 'load', do_on_load);
