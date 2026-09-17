const publicationHeader = document.getElementById('publication-name');
const category = document.getElementById('report-category');
const title = document.getElementById('report-title');
const description = document.getElementById('report-description');
const period = document.getElementById('report-period');
const generatedAt = document.getElementById('report-generated-at');
const model = document.getElementById('report-model');
const summaryContent = document.getElementById('summary-content');
const sections = document.getElementById('report-sections');
const sourcesList = document.getElementById('sources-list');
const publicationFooter = document.getElementById('footer-publication');
const footerNote = document.getElementById('footer-note');

async function getJSONData() {
  const response = await fetch("./temp/news.json");
  return await response.json();
}

const newsJSON = await getJSONData();

console.log(newsJSON);

publicationHeader.innerText = newsJSON.publication;
category.innerText = newsJSON.category;
title.innerText = newsJSON.title;

for (const i of newsJSON.introduction){
    const p = document.createElement('p');
    p.innerText = i;
    description.appendChild(p);
}

period.innerText = new Date(newsJSON.metadata.period.start).toString() + ' - ' + new Date(newsJSON.metadata.period.end).toString();
generatedAt.innerText = new Date(newsJSON.metadata.generatedAt).toString();
model.innerText = newsJSON.metadata.model;

for (const i of newsJSON.summary.paragraphs){
    const p = document.createElement('p');
    p.innerText = i;
    summaryContent.appendChild(p);
}

for (const [sectionIndex, sectionData] of newsJSON.sections.entries()) {
    const section = document.createElement('section');
    section.className = 'report-section';

    const heading = document.createElement('div');
    heading.className = 'section-heading';

    const number = document.createElement('span');
    number.className = 'section-number';
    number.innerText = String(sectionIndex + 1).padStart(2, '0');

    const sectionTitle = document.createElement('h2');
    sectionTitle.innerText = sectionData.title;
    heading.append(number, sectionTitle);
    section.appendChild(heading);

    const content = document.createElement('div');
    content.className = 'section-content';

    for (const topicData of sectionData.topics) {
        const topic = document.createElement('div');
        topic.className = 'topic';

        if (topicData.title) {
            const topicTitle = document.createElement('h3');
            topicTitle.innerText = topicData.title;
            topic.appendChild(topicTitle);
        }

        const prose = document.createElement('div');
        prose.className = 'prose';

        for (const paragraph of topicData.paragraphs) {
            const p = document.createElement('p');
            p.innerText = paragraph;
            prose.appendChild(p);
        }

        if (topicData.bullets?.length) {
            const list = document.createElement('ul');

            for (const bullet of topicData.bullets) {
                const item = document.createElement('li');
                item.innerText = bullet;
                list.appendChild(item);
            }

            prose.appendChild(list);
        }

        topic.appendChild(prose);
        content.appendChild(topic);
    }

    section.appendChild(content);
    sections.appendChild(section);
}

for (const sourceData of newsJSON.sources.items) {
    const item = document.createElement('li');

    const link = document.createElement('a');
    link.innerText = sourceData.title;
    link.href = sourceData.url;

    const sourceMeta = document.createElement('p');
    sourceMeta.className = 'source-meta';
    sourceMeta.innerText = new Date(sourceData.publishedAt).toString();

    item.append(link, sourceMeta);
    sourcesList.appendChild(item);
}

publicationFooter.innerText = newsJSON.publication;

for (const paragraph of newsJSON.footer.paragraphs) {
    const p = document.createElement('p');
    p.innerText = paragraph;
    footerNote.appendChild(p);
}
