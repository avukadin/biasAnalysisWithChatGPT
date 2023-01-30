import {ChatGPTAPIBrowser} from "chatgpt";
import * as CSV from "csv-string";
import fs from "fs";

class ChatGPTBot {
	queryDelay = 3;
	constructor(email, password) {
		this.email = email;
		this.password = password;
	}

	async init() {
		this.api = new ChatGPTAPIBrowser({
			email: this.email,
			password: this.password,
		});
		await this.api.initSession();
	}

	async makeQueries(snippetsFile, questions) {
		const data = this.readCSV(snippetsFile);

		let lastQueryTime = performance.now();
		for (let question of questions) {
			for (let i = 0; i < data["snippets"].length; i++) {
				let q = question.replace("{term}", data["terms"][i]);
				let input = q + "\n" + snippets["snippets"][i];
				const timeToWait =
					this.queryDelay - (performance.now() - lastQueryTime);
				if (timeToWait > 0) {
					await this.sleep(timeToWait);
				}

				// Make Query
				const result = await this.api.sendMessage(input);
				const response = result.response.lower().replace(".", "");
				lastQueryTime = performance.now();
				console.log(response);
			}
		}
	}

	readCSV(file) {
		const data = fs.readFileSync(file, "utf8");
		const arr = CSV.parse(data);

		const out = new Map();
		const colNames = arr[0];
		colNames.map((h) => (out[h] = []));

		for (let i = 1; i < arr.length; i++) {
			let row = arr[i];
			row.map((v, i) => out[colNames[i]].push(v));
			if (i > 2) {
				break;
			}
		}
		return out;
	}

	sleep(seconds) {
		return new Promise((resolve) => setTimeout(resolve, seconds * 1000));
	}
}

const EMAIL = "<your_email>";
const PASSWWORD = "<your_password>";

var c = new ChatGPTBot(EMAIL, PASSWWORD);
await c.init();
c.makeQueries("./data/articles_snippets.csv", [
	"Does this news show {term} in a positive, negative or neutral way? Answer in one word.",
]);
c.readCSV("./data/articles_snippets.csv");
