const log = require("json-log").log;
const config = require('config')

interval = config.interval
count = config.count
max = config.maxNum

log.info("Starting rando app!");
log.info(`Interval: ${interval}`)
log.info(`Count: ${count}`)
log.info(`MaxNum: ${max}`)

async function main() {
  colors = ["red", "orange", "yellow", "green", "blue", "purple"]
  while (true) {
    // Set values (defined or random)
    if (interval != "random")
    {
      thisInterval = interval
    }
    else {
      thisInterval = getRandomInt(120)
    }

    if (count != "random")
    {
      thisCount = interval
    }
    else {
      thisCount = getRandomInt(50)
    }

    // Write "thisCount" random log lines
    for (i = 0; i < thisCount; i++) {
      num = getRandomInt(max)
      color = colors[getRandomInt(6)]
      log.info("Random data", { rando_details: { color: color , number: num} });
    }

    // Sleep for "thisInterval" seconds
    await sleep(thisInterval*1000);

  }
}

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

main();