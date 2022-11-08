const duckdb = require('duckdb')
const {readFileSync} = require('fs');
const {join} = require('path');

let duckdb_package = join(require.resolve('duckdb'), '../../package.json');
let pkg_json = JSON.parse(readFileSync(duckdb_package).toString());
console.log('duckdb version:', pkg_json.version);
console.log('arch:', process.arch);

const db = new duckdb.Database(":memory:");

async function main() {
    console.log('Program Started ...');
    try {
        const res = await new Promise((resolve, reject) =>
            db.all("SELECT CAST('11:10:10' AS BAD_TYPE) as time", (err, res) => err ? reject(err) : resolve(res))
        );
        console.log(`We got results : ${res[0]}`);
    } catch (error) {
        console.log(`Caught Error: ${error}`);
    }
    console.log('Program exited cleanly!');
}

main().then(r => console.log('exited'));
