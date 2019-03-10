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
var  lastQuestion = "";
var lastAnswer = "";
var responseIdx = 0;
var btn_id = 0;
var exclude_feedback_qs = [
    "help"
];
var exclude_feedback_answers = [
    "Sorry, I don't know anything else about this.".toLowerCase(),
    "I am sorry, but I do not understand.".toLowerCase()
];

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
    } else {
        lastAnswer = text;
    }
}

function getAlternateResponse() {
    if(lastQuestion === "") {
        warn("Oops!", "It looks like you haven't asked any other questions yet.");
    } else {
        appendChatMsg("alternate response", true);
        responseIdx++;

        $.get("/get", {msg: lastQuestion, alt_response: responseIdx}).done(function (data) {
            hideSpinner();
            var fb_a = !exclude_feedback_answers.includes(data.toLowerCase().trim());
            appendChatMsg(data, false, fb_a);
            $('pre code').each(function(i, e) { hljs.highlightBlock(e) });
        });
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
        lastQuestion = rawText;
        appendChatMsg(rawText, true);

        $.get("/get", {msg: rawText}).done(function (data) {
            hideSpinner();
            var fb_q = !exclude_feedback_qs.includes(rawText.toLowerCase().trim());
            var fb_a = !exclude_feedback_answers.includes(data.toLowerCase().trim());
            console.log(data);
            appendChatMsg(data, false, fb_q && fb_a);
            $('pre code').each(function(i, e) { hljs.highlightBlock(e) });
        });
    }
}

function getFeedback(id, feedback) {
    var div = $(id);
    var parent = div.parent();
    div.remove();
    parent.append(spinnerHtml);

    $.get("/get", { msg: "FEEDBACK", rating: feedback, question: lastQuestion, answer: lastAnswer }).done(function (data) {
            hideSpinner();
            parent.append(feedbackMsgHtml);
    });
}


$(document).ready(function() {
    hljs.configure({languages: ['C++', 'C']});

    $("#buttonInput").click(function() {
        let rawText = textInput.val();
        textInput.val("");
        getBotResponse(rawText);
    });

    textInput.keypress(function(e) {
        let rawText = textInput.val();
        if(e.which === 13) {
            textInput.val("");
            getBotResponse(rawText);
        }
    });

    $('#helpLink').click(function () {
        getBotResponse("Help");
    });
});