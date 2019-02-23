// render static templates as they do 
// not need to be re-rendered every time
// they are used
var spinnerTmpl = $.templates("#spinnerTmpl");
var spinnerHtml = spinnerTmpl.render();
var feedbackTmpl = $.templates('#feedbackTmpl');
var feedbackHtml = feedbackTmpl.render();

// preselect necessary divs
var chatbox =  $("#chatbox");
var textInput = $("#textInput");
var lastMsg = "";
var responseIdx = 0;

// use different delimiters than jinja's
// to avoid errors
$.views.settings.delimiters("<%", "%>");

function showSpinner() {
    chatbox.append(spinnerHtml);
}

function hideSpinner() {
    chatbox.children('.sk-three-bounce').remove();
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
    data = {
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
    var data = {text: text};
    if(user) {
        data.bg_col = "info";
    } else {
        data.bg_col = "dark";
    }
    var messageTmpl = $.templates('#messageTmpl');
    var messageHtml = messageTmpl.render(data);
    chatbox.append(messageHtml);
    if(feedback) {
        chatbox.children().last().append(feedbackHtml);
    }
    chatbox.animate({ scrollTop: chatbox[0].scrollHeight }, 1000);
    if(user)
        showSpinner();
}

function getAlternateResponse() {
    if(lastMsg === "") {
        warn("Oops!", "It looks like you haven't asked any other questions yet.");
    } else {
        appendChatMsg("alternate response", true);
        responseIdx++;
        if(responseIdx > 2) {
            hideSpinner();
            chatbox.appendChatMsg("I don't know anything else about this", false);
        } else {
            $.get("/get", {msg: lastMsg, alt_response: responseIdx}).done(function (data) {
                hideSpinner();
                appendChatMsg(data, false, true);
            });
        }
    }
}

function getBotResponse(rawText) {
    if(rawText === "") {
        warn("Oops!", "It looks like you haven't a asked a question.");
        chatbox.animate({ scrollTop: chatbox[0].scrollHeight }, 1000);
    } else if(rawText.toLowerCase() === "alternate response") {
        getAlternateResponse()
    } else {
        responseIdx = 0;
        // rawText = fixTypos(rawText, "en-us");
        lastMsg = rawText;
        appendChatMsg(rawText, true);
        $.get("/get", {msg: rawText}).done(function (data) {
            hideSpinner();
            appendChatMsg(data, false, true);
            $('pre code').each(function(i, e) {hljs.highlightBlock(e)});
        });
    }
}

$(document).ready(function() {
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