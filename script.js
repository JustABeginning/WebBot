(function () {
    function onTidioChatApiReady() {
        // Code after chat loaded
        $(document).ready(function () {
            $("#query").keypress(function (e) {
                var code = (e.keyCode ? e.keyCode : e.which);
                if (code == 13) {
                    $("#submit").trigger('click');
                    return true;
                }
            });
            $("#submit").click(async function () {
                var query = document.getElementById("query").value;
                query = query.trim();
                if (query.length > 0) {
                    $.ajax({
                        url: await waitForAns(query),
                        success: function () {
                            // Get RESPONSE from OpenAI
                            getAnswer(query);
                        }
                    });
                }
            });
        });
    }
    if (window.tidioChatApi) {
        window.tidioChatApi.on("ready", onTidioChatApiReady);
    } else {
        document.addEventListener("tidioChat-ready", onTidioChatApiReady);
    }
    function waitForAns(query) {
        return new Promise((resolve) => {
            setTimeout(() => {
                document.getElementById("query").value = "";
                tidioChatApi.messageFromVisitor(query);
                document.getElementById("answer").value = "\n\tResponse LOADING . . .";
                resolve(0);
            }, 500);
        });
    }
    function getAnswer(query) {
        const answer = runPyScript(query);
        document.getElementById("answer").value = answer;
        tidioChatApi.messageFromOperator(answer);
    }
    function runPyScript(input) {
        var jqXHR = $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/login",
            async: false,
            data: {mydata: input}
        });
        return jqXHR.responseText;
    }
})();
