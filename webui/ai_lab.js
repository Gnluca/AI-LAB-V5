async function loadRuntime(){

    const r =
        await fetch(
            "/runtime/master-loop"
        );

    const data =
        await r.json();

    document
        .getElementById("runtime")
        .textContent =
        JSON.stringify(
            data,
            null,
            2
        );
}

async function loadCognitive(){

    const r =
        await fetch(
            "/runtime/cognitive-report"
        );

    const data =
        await r.json();

    document
        .getElementById("cognitive")
        .textContent =
        JSON.stringify(
            data,
            null,
            2
        );
}

async function loadFeedback(){

    const r =
        await fetch(
            "/runtime/feedback"
        );

    const data =
        await r.json();

    document
        .getElementById("feedback")
        .textContent =
        JSON.stringify(
            data,
            null,
            2
        );
}

async function refresh(){

    await loadRuntime();
    await loadCognitive();
    await loadFeedback();
}

refresh();

setInterval(
    refresh,
    5000
);