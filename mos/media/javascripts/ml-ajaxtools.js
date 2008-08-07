function submit_form(type, id){
    myform = $(type + '-form-' + id);
    new Ajax.Updater($(type + 'container' + id), myform.readAttribute('action'), {
                  parameters: myform.serialize(true),
    });
 
}

function delete_entry(type, id, came_from){
    myform = $(type + '-form-' + id);

    new Ajax.Updater( $(type + '-content'), '/' + type + '/'  + id + '/delete/' + came_from + '/', {
        parameters: myform.serialize(true),
    });
    
}
   

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


function do_on_load()
{
//    update_metasense();
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


function submit_event(id) {
    var frm = $('calendar-form-'+id);
    var cnt = $('calendar-edit-'+id);

    new Ajax.Request(frm.readAttribute('action'), {
                                                    parameters: frm.serialize(true),
                                                    onSuccess: function(r) {
                                                                            new Ajax.Updater('calendar-content', calendarUpdateURL);
                                                                           },
                                                    onFailure: function(r) {
                                                                            cnt.innerHTML = r.responseText;
                                                                            DateTimeShortcuts.init.defer(1);
                                                                           }
                                                  })
}
