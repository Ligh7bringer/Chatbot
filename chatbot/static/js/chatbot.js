// render static templates as they do
// not need to be re-rendered every time
// they are used
let spinnerTmpl = $.templates("#spinnerTmpl");
let spinnerHtml = spinnerTmpl.render();
let feedbackMsgTmpl = $.templates("#feedbackMsgTmpl");
let feedbackMsgHtml = feedbackMsgTmpl.render();

// preselect necessary divs
let chatbox =  $("#chatbox");
let textInput = $("#textInput");

let exclude_feedback_qs = [
    "help"
];
let exclude_feedback_answers = [
    "Sorry, I don't know anything else about this.".toLowerCase(),
    "I am sorry, but I do not understand.".toLowerCase()
];

// global variables
let  lastQuestion = "";
let lastAnswer = "";
let responseIdx = 0;
let btn_id = 0;

let cache = [];

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

    let warningTmpl = $.templates('#warningTmpl');
    let warningHtml = warningTmpl.render(data);
    chatbox.append(warningHtml);
    hideWarning();
}

function sendRequest(data) {
    // to do
}

function appendChatMsg(text, user, feedback=false) {
    let data = {
        "text": text,
        "bg_col": user ? "info" : "dark"
    };

    let messageTmpl = $.templates('#messageTmpl');
    let messageHtml = messageTmpl.render(data);

    chatbox.append(messageHtml);

    if(feedback) {
        console.log("btn id: ", btn_id);

        let feedbackTmpl = $.templates('#feedbackTmpl');
        let feedbackData = {
            "btn_id": btn_id
        };

        btn_id++;

        let feedbackHtml = feedbackTmpl.render(feedbackData);
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
            let fb_a = !exclude_feedback_answers.includes(data.toLowerCase().trim());

            appendChatMsg(data, false, fb_a);

            if(fb_a) {
                cache.push([lastQuestion, data]);
                console.log(cache);
            }

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

            // can feedback be given for this question
            let fb_q = !exclude_feedback_qs.includes(rawText.toLowerCase().trim());
            // can feedback be given for this answer
            let fb_a = !exclude_feedback_answers.includes(data.toLowerCase().trim());

            appendChatMsg(data, false, fb_q && fb_a);

            if(fb_a) {
                cache.push([rawText, data]);
                console.log(cache);
            }

            $('pre code').each(function(i, e) { hljs.highlightBlock(e) });
        });
    }
}

// this function is called from the onClick property
// of the buttons in chatbot.html
function getFeedback(id, feedback) {
    console.log(id);
    let div = $(id);
    let parent = div.parent();

    div.remove();
    parent.append(spinnerHtml);

    let idx = id[id.length-1];
    let q = cache[idx][0];
    let a = cache[idx][1];
    console.log(idx, q, a);

    $.get("/get",
         { msg: "FEEDBACK", rating: feedback, question: q, answer: a }).done(function (data) {
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