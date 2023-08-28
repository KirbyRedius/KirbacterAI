js_simple_request = """
async () => {
	const payload = {
		method: "MY_METHOD",
		headers: MY_HEADERS,
		body: JSON.stringify(MY_BODY)
	}
	const response = await window.fetch("MY_URL", payload)

	const data = await response.text();
	const matches = data.match(/\{.*\}/g);

	const responseText = matches[matches.length - 1];

	let result = {
		code: 500,
	};

	if (!matches) result = null;
	else {
		result.code = 200
		result.response = responseText
	}

	return result.response;
}
"""