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
                    document.getElementById("query").value = "";
                    tidioChatApi.messageFromVisitor(query);
                    document.getElementById("answer").value = "\n\tResponse LOADING . . .";
                    // Get RESPONSE from OpenAI
                    const API_KEY = "OpenAI_API_KEY";
                    const API_URL = "https://api.openai.com/v1/completions";
                    const options = {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${API_KEY}`,
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            model: "text-davinci-003",
                            prompt: query,
                            max_tokens: 500,
                            temperature: 0.65,
                            frequency_penalty: 0.5,
                            presence_penalty: 0.5,
                            best_of: 3
                        }),
                    };
                    try {
                        const response = await fetch(API_URL, options);
                        const responseJson = await response.json();
                        var answer = responseJson.choices[0].text;
                        // Process ANSWER
                        answer = answer.trim();
                        document.getElementById("answer").value = answer;
                        tidioChatApi.messageFromOperator(answer);
                    } catch (error) {
                        console.error("\nError in RESPONSE :=> ", error);
                    }
                }
            });
        });
    }
    if (window.tidioChatApi) {
        window.tidioChatApi.on("ready", onTidioChatApiReady);
    } else {
        document.addEventListener("tidioChat-ready", onTidioChatApiReady);
    }
})();
