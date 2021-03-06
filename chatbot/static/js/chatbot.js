// prerender the spinner template
// as it doesn't change
const spinnerTmpl = $.templates("#spinnerTmpl");
const spinnerHtml = spinnerTmpl.render();

// preselect necessary divs
let chatbox = $("#chatbox");
let textInput = $("#textInput");
let sendingRequest = false;

const exclude_feedback_qs = [
    "help"
];
const exclude_feedback_answers = [
    "Sorry, I don't know anything else about this.".toLowerCase(),
    "I am sorry, but I do not understand.".toLowerCase()
];

// global variables
let btn_id = 0;
let cache = [];

// use different delimiters than jinja's
// to avoid errors
$.views.settings.delimiters("<%", "%>");

String.prototype.isEmpty = String.prototype.isEmpty || function() {
    return !(!!this.trim().length);
};

function resizeImages() {
    $('img').addClass('img-fluid');
}

// shows the loading animation
function showSpinner() {
    chatbox.append(spinnerHtml);
}

// hides the loading animation
function hideSpinner() {
    $('.sk-three-bounce').remove();
}

// hides a warning message after 2 seconds
function hideWarning() {
    window.setTimeout(function() {
        $(".alert").fadeTo(500, 0).slideUp(500, function() {
            $(this).remove();
        });
    }, 2500);
}

// shows a warning message
function warn(title, message) {
    textInput.val("");

    let data = {
        title: title,
        body: message
    };

    const warningTmpl = $.templates('#warningTmpl');
    const warningHtml = warningTmpl.render(data);
    chatbox.append(warningHtml);
    hideWarning();
}

function removeAltResponseBtns() {
    // remove alternate response buttons
    // except the last one
    let btns = $('.alt-response-btn');
    for (let i = 0; i < btns.length; i++) {
        btns[i].remove();
    }

    let ors = $('.or');
    for (let i = 0; i < ors.length; i++) {
        ors[i].remove();
    }
}

// adds a user or bot message to the chatbox
function appendChatMsg(text, user, feedback = false) {
    const data = {
        "text": text,
        "bg_col": user ? "user" : "darker"
    };

    const messageTmpl = $.templates('#messageTmpl');
    const messageHtml = messageTmpl.render(data);

    $(messageHtml).appendTo(chatbox).hide().fadeIn(700);

    if (feedback) {
        const feedbackTmpl = $.templates('#feedbackTmpl');
        const feedbackData = {
            "btn_id": btn_id
        };

        btn_id++;

        const feedbackHtml = feedbackTmpl.render(feedbackData);
        chatbox.children().last().append(feedbackHtml);
    }

    // if this is a message sent by the user
    if (user) {
        // scroll down to it
        chatbox.animate({
            scrollTop: chatbox[0].scrollHeight
        }, 1000);
        showSpinner();
    }
}

// sends a request to the backend program
function sendRequest(data) {
    $('#buttonInput').prop('disabled', true);
    sendingRequest = true;
    $.get("/get", data).done(function(response) {
        hideSpinner();

        // can feedback be given for this question
        const fb_q = !exclude_feedback_qs.includes(lastQuestion.toLowerCase().trim());
        // can feedback be given for this answer
        const fb_a = !exclude_feedback_answers.includes(response.toLowerCase().trim());

        appendChatMsg(response, false, fb_q && fb_a);

        if (fb_q && fb_a) {
            cache.push([lastQuestion, response]);
        }

        resizeImages();
        $('pre code').each(function(i, e) {
            hljs.highlightBlock(e)
        });
        $('#buttonInput').prop('disabled', false);
        sendingRequest = false;
    });
}

// returns another response to the last question that was asked
function getAlternateResponse() {
    if (!lastQuestion) {
        warn("Oops!", "It looks like you haven't asked any other questions yet.");
    } else {
        appendChatMsg("alternate response", true);

        const data = {
            request_type: "alternate"
        };

        sendRequest(data);
    }
}

// returns a response to the question the user asked
function getBotResponse(rawText) {
    if (!sendingRequest) {
        if (rawText.isEmpty()) {
            warn("Oops!", "It looks like you haven't a asked a question.");
            chatbox.animate({
                scrollTop: chatbox[0].scrollHeight
            }, 1000);
        } else if (rawText.toLowerCase() === "alternate response") {
            getAlternateResponse();
        } else {
            lastQuestion = rawText;
            appendChatMsg(rawText, true);

            const data = {
                request_type: "regular",
                msg: rawText
            };
            sendRequest(data);
        }
    }
    removeAltResponseBtns();
}

// this function is called from the onClick property
// of the buttons in chatbot.html
function getFeedback(id, feedback) {
    let div = $(id);
    let parent = div.parent();

    div.remove();
    parent.append(spinnerHtml);

    const idx = id[id.length - 1];
    const q = cache[idx][0];
    const a = cache[idx][1];

    const requestBody = {
        request_type: "feedback",
        rating: feedback,
        answer: a
    };

    const feedbackMsgTmpl = $.templates("#feedbackMsgTmpl");
    let feedbackMsgHtml;
    const feedback_no = feedback === 'no';
    const template_data = {
        "feedback_no": feedback_no
    };

    feedbackMsgHtml = feedbackMsgTmpl.render(template_data);

    $.get("/get", requestBody).done(function(data) {
        hideSpinner();
        parent.append(feedbackMsgHtml);
    });
}

// executed when the page is fully loaded
$(document).ready(function() {
    // hide the help menu button in the about page
    // a it can't be used in it
    const pathname = window.location.pathname;
    if (pathname === '/about') {
        $("#nav-help-link").remove();
    }

    // check if the Send button is clicked
    $("#buttonInput").click(function() {
        let rawText = textInput.val();
        // wait until the current request is finished
        if (!sendingRequest) {
            textInput.val("");
            getBotResponse(rawText);
        }
    });

    // check if Enter is pressed in the text input
    textInput.keypress(function(e) {
        let rawText = textInput.val();
        // if enter is pressed
        // and a request is not currently being sent
        if (e.which === 13 && !sendingRequest) {
            textInput.val("");
            getBotResponse(rawText);
        }
    });

    // check if the help link is clicked
    $('.helpLink').click(function() {
        getBotResponse("Help");
    });
});