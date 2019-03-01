// render static templates as they do 
// not need to be re-rendered every time
// they are used
var spinnerTmpl = $.templates("#spinnerTmpl");
var spinnerHtml = spinnerTmpl.render();
var feedbackMsgTmpl = $.templates("#feedbackMsgTmpl");
var feedbackMsgHtml = feedbackMsgTmpl.render();

// preselect necessary divs
var chatbox =  $("#chatbox");
var textInput = $("#textInput");

// global variables
var lastMsg = "";
var responseIdx = 0;
var btn_id = 0;

// use different delimiters than jinja's
// to avoid errors
$.views.settings.delimiters("<%", "%>");

function showSpinner() {
    chatbox.append(spinnerHtml);
}

function hideSpinner() {
    $('.sk-three-bounce').remove();
}

function hideWarning() {
    window.setTimeout(function() {
        $(".alert").fadeTo(500, 0).slideUp(500, function(){
            $(this).remove();
        });
    }, 2000);
}

function warn(title, message) {
    textInput.val("");
    let data = {
        title: title,
        body: message
    };
    var warningTmpl = $.templates('#warningTmpl');
    var warningHtml = warningTmpl.render(data);
    chatbox.append(warningHtml);
    hideWarning();
}

function appendChatMsg(text, user, feedback=false) {
    textInput.val("");
    var data = {
        "text": text,
        "bg_col": user ? "info" : "dark"
    };
    var messageTmpl = $.templates('#messageTmpl');
    var messageHtml = messageTmpl.render(data);
    chatbox.append(messageHtml);
    if(feedback) {
        var feedbackTmpl = $.templates('#feedbackTmpl');
        var feedbackData = {
            "btn_id": btn_id
        };
        btn_id++;
        var feedbackHtml = feedbackTmpl.render(feedbackData);
        chatbox.children().last().append(feedbackHtml);
    }
    if(user) {
        chatbox.animate({ scrollTop: chatbox[0].scrollHeight }, 1000);
        showSpinner();
    }
}

function getAlternateResponse() {
    if(lastMsg === "") {
        warn("Oops!", "It looks like you haven't asked any other questions yet.");
    } else {
        appendChatMsg("alternate response", true);
        responseIdx++;
        if(responseIdx > 2) {
            hideSpinner();
            appendChatMsg('I don\'t know anything else about <strong><i>' + lastMsg + '</i></strong>.', false);
        } else {
            $.get("/get", {msg: lastMsg, alt_response: responseIdx}).done(function (data) {
                hideSpinner();
                appendChatMsg(data, false, true);
                $('pre code').each(function(i, e) { hljs.highlightBlock(e) });
            });
        }
    }
}

function getBotResponse(rawText) {
    if(rawText === "") {
        warn("Oops!", "It looks like you haven't a asked a question.");
        chatbox.animate({ scrollTop: chatbox[0].scrollHeight }, 1000);
    } else if(rawText.toLowerCase() === "alternate response") {
        getAlternateResponse();
    } else {
        responseIdx = 0;
        lastMsg = rawText;
        appendChatMsg(rawText, true);
        $.get("/get", {msg: rawText}).done(function (data) {
            hideSpinner();
            var feedback = rawText.toLowerCase() !== "help";
            appendChatMsg(data, false, feedback);
            $('pre code').each(function(i, e) { hljs.highlightBlock(e) });
        });
    }
}

function getFeedback(id, feedback){
    var div = $(id);
    var parent = div.parent();
    div.remove();
    parent.append(spinnerHtml);
    $.get("/get", {msg: "FEEDBACK", rating: feedback, question: lastMsg}).done(function (data) {
        hideSpinner();
        parent.append(feedbackMsgHtml);
    });
}


$(document).ready(function() {
    hljs.configure({languages: ['C++', 'C']});

    $("#buttonInput").click(function() {
        let rawText = textInput.val();
        getBotResponse(rawText);
    });

    textInput.keypress(function(e) {
        let rawText = textInput.val();
        if(e.which === 13) {
            getBotResponse(rawText);
        }
    });

    $('#helpLink').click(function () {
        getBotResponse("Help");
    });
});