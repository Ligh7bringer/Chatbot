const userDiv = '<div class="p-3 mb-2 bg-info text-white rounded">';
const botDiv = '<div id="botText" class="p-3 mb-2 bg-dark text-white rounded">';
const loadDiv = '<div class="sk-three-bounce"><div class="sk-child sk-bounce1"></div><div class="sk-child sk-bounce2"></div>';                      'div class="sk-child sk-bounce3"></div></div>';
const warningBegin = '<div class="alert alert-danger alert-dismissible fade show" role="alert">';
const warningEnd = '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                    '<span aria-hidden="true">&times;</span>' +
                    '</button></div>';
const noQuestions = '<strong>Oops!</strong> It looks like you haven\'t asked a question!';
const noLastMsg = "<strong>Oops!</strong> Try asking a question first and then requesting an alternate answer.";
const feedbackBtns = '<div class="row">' +
                    '<div class="col-sm-4 my-auto"><strong>Was this answer helpful?</strong></div>' +
                    '<div class="col-sm-6">' +
                    '<div class="btn-group mr-2" role="group" aria-label="First group">' +
                    '<button type="button" class="btn btn-success custom-button-width .navbar-right">Yes</button> </div>' +
                    '<div class="btn-group mr-2" role="group" aria-label="First group">' +
                    '<button type="button" class="btn btn-danger custom-button-width .navbar-right">No</button> </div>' +
                    '</div>' +
                    '</div></div>';

let chatbox =  $("#chatbox");
let textInput = $("#textInput");
let lastMsg = "";
let responseIdx = 0;

function warn(body) {
    let warning = warningBegin + body + warningEnd;
    chatbox.append(warning);
    window.setTimeout(function() {
            $(".alert").fadeTo(500, 0).slideUp(500, function(){
                $(this).remove();
            });
        }, 2000);
}

function appendUserMsg(rawText) {
    const userHtml =  userDiv + rawText + '</div>';
    textInput.val("");
    chatbox.append(userHtml);
    chatbox.animate({ scrollTop: chatbox[0].scrollHeight }, 1000);
    chatbox.append(loadDiv);
}

function getAlternateResponse() {
    if(lastMsg === "") {
        warn(noLastMsg);
    } else {
        appendUserMsg("alternate response");
        responseIdx++;
        if(responseIdx > 2) {
            chatbox.children().last().remove();
            let botHtml = botDiv + 'I don\'t know anything else about <i>"' + lastMsg + '"</i></div>.';
            chatbox.append(botHtml);
        } else {
            $.get("/get", {msg: lastMsg, alt_response: responseIdx}).done(function (data) {
                chatbox.children().last().remove();
                const botHtml = botDiv + data + '</div>';
                chatbox.append(botHtml);
            });
        }
    }
}

function getBotResponse(rawText) {
    if(rawText === "") {
        warn(noQuestions);
        chatbox.animate({ scrollTop: chatbox[0].scrollHeight }, 1000);
    } else if(rawText.toLowerCase() === "alternate response") {
        getAlternateResponse()
    } else {
        responseIdx = 0;
        rawText = fixTypos(rawText, "en-us");
        lastMsg = rawText;
        appendUserMsg(rawText);
        $.get("/get", {msg: rawText}).done(function (data) {
            const botHtml = botDiv + data + '<hr id="nine">' + feedbackBtns + '</div>';
            chatbox.children().last().remove();
            chatbox.append(botHtml);
            $('pre code').each(function(i, e) {hljs.highlightBlock(e)});
        });
    }
}

textInput.keypress(function(e) {
    let rawText = textInput.val();
    if(e.which === 13) {
        getBotResponse(rawText);
    }
});

$(document).ready(function() {
    $("#buttonInput").click(function() {
        let rawText = textInput.val();
        getBotResponse(rawText);
    });

    $('#helpLink').click(function () {
        getBotResponse("Help");
    });
});