const fs = require("fs");
const csv = require("csv-parser");

function loadEmails(filepath,limit = 7000) {
    return new Promise((resolve,reject) => {
        const data = [];
        let count = 0;
        fs.createReadStream(filepath)
        .on("error", reject)
        .pipe(csv())
        .on("data",(row) =>  {
            if (count >= limit) return;
            const rawLabel = (row["Spam/Ham"] || "").toString().trim().toLowerCase();
            const subject = (row["Subject"] || "").toString().trim();
            const message = (row["Message"] || "").toString().trim();
            
     

        const label = 
        rawLabel === "spam" ? "Spam":
        rawLabel === "ham" ? "Not Spam":
        null;
// chat start
const text = `${subject} ${message}`.trim();

// SKIP massive emails (this is the key fix)
if (!label || text.length < 3 || text.length > 2000) return;

data.push({ text, label });
count++
//chat end
        })
        .on("end", () => resolve(data))
        .on("error",reject);
    });
};
module.exports = {loadEmails};