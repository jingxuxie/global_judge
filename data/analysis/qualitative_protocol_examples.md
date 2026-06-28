# Qualitative Protocol Examples

Generated from the main candidate-quality n=50 run. Scores use the 1-5 judge scale.

Protocol score columns are direct, target-language rubric, explicit English pivot, and bilingual rubric.

## Pivot inflates human-negative item

### vi / comprehensibility / human label 0

- Item: `seahorse_test_vi_comprehensibility_008948_reference`
- Scores: direct=2, target=2, pivot=5, bilingual=1
- Original summary: Chuẩn bị vật liệu,.
- English pivot: Prepare materials.
- Target-rubric rationale: Câu tóm tắt không rõ ràng và thiếu thông tin cần thiết để người đọc hiểu nội dung.
- Pivot rationale: The summary is clear and straightforward, conveying a simple action.
- Bilingual rationale: Summary is unclear and lacks context for understanding.

### tr / grammar / human label 0

- Item: `seahorse_test_tr_grammar_008888_mt5_small`
- Scores: direct=2, target=3, pivot=5, bilingual=2
- Original summary: Kuzey Kore lideri Kim Jong-nam'ın kardeşi Kim Jong-nam'ın, bir kamera şakası yaptığını iddia eden bir kişi gözaltına alındı.
- English pivot: A person claiming to be a prankster of Kim Jong-nam, the brother of North Korean leader Kim Jong-un, has been detained.
- Target-rubric rationale: Cümledeki isimlerin tekrarı ve yapı açısından bazı karmaşalar var, ancak genel anlamda anlaşılır ve akıcı.
- Pivot rationale: The summary is grammatical and fluent in English.
- Bilingual rationale: Cümlede isim karışıklığı ve dilbilgisi hatası var.

### tr / grammar / human label 0

- Item: `seahorse_test_tr_grammar_008780_mt5_small`
- Scores: direct=3, target=2, pivot=5, bilingual=3
- Original summary: ABD'li avukat James Comet'in, teknoloji devi Microsoft'un yeni filmini yapan ve ünlü yönetmenlerinden Erik Spielberg, yeni film için bir araya geldi.
- English pivot: American lawyer James Comet met with Erik Spielberg, the famous director, who is making a new film for the technology giant Microsoft. They came together for the new film.
- Target-rubric rationale: Cümlede dilbilgisi hataları var ve akıcılık açısından zayıf. Özellikle 'yeni filmini yapan' ifadesi belirsiz ve karışık.
- Pivot rationale: The summary is grammatical and fluent in English.
- Bilingual rationale: Cümle yapısı karmaşık, bazı dilbilgisi hataları var.

### tr / grammar / human label 0

- Item: `seahorse_test_tr_grammar_004303_mt5_small_250steps`
- Scores: direct=4, target=2, pivot=5, bilingual=4
- Original summary: Facebook’ı aç. Hoşlandığın kişinin adını bul.
- English pivot: Open Facebook. Find the name of the person you like.
- Target-rubric rationale: Cümle dilbilgisi açısından bazı eksiklikler ve akıcılık sorunları içeriyor.
- Pivot rationale: The summary is clear, grammatical, and fluent in English.
- Bilingual rationale: Dilbilgisi doğru, akıcılık iyi seviyede.

### vi / grammar / human label 0

- Item: `seahorse_test_vi_grammar_008693_mt5_xxl`
- Scores: direct=4, target=2, pivot=5, bilingual=4
- Original summary: Một đoạn phim video mới quay cảnh treo cổ cựu tổng thống Iraq Saddam Hussein được tung ra trên mạng internet.
- English pivot: A new video clip showing the hanging of former Iraqi president Saddam Hussein has been released on the internet.
- Target-rubric rationale: Câu văn không sử dụng đúng ngữ pháp và có cấu trúc không rõ ràng, gây khó hiểu cho người đọc.
- Pivot rationale: The summary is clear, grammatical, and fluent in English.
- Bilingual rationale: Câu văn sử dụng ngữ pháp đúng và có tính mạch lạc.

### vi / grammar / human label 0

- Item: `seahorse_test_vi_grammar_006238_mt5_small`
- Scores: direct=4, target=2, pivot=5, bilingual=3
- Original summary: Thính giả Phan Xuân Trung đã tới Luân Đôn để nghe tin tức về vụ nổ bom đạn nổ trên đất nước.
- English pivot: Listener Phan Xuan Trung has arrived in London to hear news about the bomb explosion in the country.
- Target-rubric rationale: Câu văn có lỗi ngữ pháp và cấu trúc không rõ ràng, gây khó hiểu cho người đọc.
- Pivot rationale: The summary is clear, grammatical, and fluent in English.
- Bilingual rationale: Câu có ngữ pháp cơ bản nhưng chưa hoàn toàn trôi chảy.

### tr / comprehensibility / human label 0

- Item: `seahorse_test_tr_comprehensibility_004062_reference`
- Scores: direct=4, target=3, pivot=5, bilingual=3
- Original summary: Unibeast klasörünü aç. Unibeast uygulamasını aç. Sorulduğunda Open (Aç) seçeneğine tıkla. Continue Sorulduğunda Agree (Kabul ediyorum) üzerine tıkla. USB diskini seç, sonra Continue (Devam et) üzerine tıkla....
- English pivot: Open the Unibeast folder. Launch the Unibeast application. When prompted, click on Open. When asked to Continue, click on Agree. Select the USB disk, then click on Continue. Choose the High Sierra motherboar...
- Target-rubric rationale: Özet, adım adım talimatlar içeriyor ancak bazı terimler ve işlemler açıklanmamış, bu da anlaşılırlığı zorlaştırıyor.
- Pivot rationale: The summary is clear and easy to follow step-by-step.
- Bilingual rationale: Özet adımları net ama bazı terimler belirsiz kalıyor.

### tr / grammar / human label 0

- Item: `seahorse_test_tr_grammar_003456_mt5_small`
- Scores: direct=3, target=4, pivot=5, bilingual=4
- Original summary: İngiltere'de hükümetin koronavirüs salgınında ölüm oranlarının Ekim ortası 50 bine çıkabileceğini açıkladı.
- English pivot: The government in the UK announced that the death toll from the coronavirus pandemic could reach 50,000 by mid-October.
- Target-rubric rationale: Cümle dilbilgisi açısından doğru ve akıcı, anlamı net bir şekilde ifade ediyor.
- Pivot rationale: The summary is grammatical and fluent in English.
- Bilingual rationale: Cümle dilbilgisi açısından doğru ve akıcı bir şekilde ifade edilmiştir.

## Pivot deflates human-positive item

### tr / comprehensibility / human label 1

- Item: `seahorse_test_tr_comprehensibility_017488_1shot`
- Scores: direct=5, target=5, pivot=1, bilingual=5
- Original summary: Kâğıdı kare şeklinde katla.
- English pivot: Fold the paper into a square shape. Fold the paper into a square shape. [repetition continues]
- Target-rubric rationale: Özet, basit ve net bir talimat veriyor, bu nedenle kolayca anlaşılabilir.
- Pivot rationale: Repetition makes the summary unclear and difficult to understand.
- Bilingual rationale: Özet, basit ve anlaşılır bir talimat sunuyor.

### es-ES / comprehensibility / human label 1

- Item: `seahorse_test_es-ES_comprehensibility_008104_mt5_small`
- Scores: direct=5, target=4, pivot=2, bilingual=4
- Original summary: La Comisión Europea detecta otros 12 sospechosos de haber combatido en las filas del Estado Islámico
- English pivot: The European Commission identifies another 12 suspects of having fought in the ranks of the Islamic State. The European Commission detects other 12 suspects of having fought in the ranks of the Islamic State...
- Target-rubric rationale: El resumen es claro y directo, facilitando la comprensión del mensaje principal sobre la detección de sospechosos por parte de la Comisió...
- Pivot rationale: Repetition affects clarity and makes it harder to understand.
- Bilingual rationale: El resumen es claro y directo, fácil de entender.

### es-ES / grammar / human label 1

- Item: `seahorse_test_es-ES_grammar_012428_finetuned`
- Scores: direct=5, target=4, pivot=2, bilingual=4
- Original summary: La oposición venezolana volvió a renacer.
- English pivot: The Venezuelan opposition has risen again. The Venezuelan opposition has come back to life. [repetition continues]
- Target-rubric rationale: El resumen es gramaticalmente correcto y fluido, aunque es muy breve.
- Pivot rationale: Repetitive phrasing affects fluency and overall grammatical quality.
- Bilingual rationale: El resumen es gramaticalmente correcto y fluido.

### es-ES / comprehensibility / human label 1

- Item: `seahorse_test_es-ES_comprehensibility_008215_mt5_small_250steps`
- Scores: direct=4, target=2, pivot=1, bilingual=2
- Original summary: Abre un modelo de barco de madera.
- English pivot: Opens a model of a wooden boat. [repetition continues]
- Target-rubric rationale: El resumen es muy breve y carece de contexto, lo que dificulta su comprensión.
- Pivot rationale: The summary is unclear and lacks coherence.
- Bilingual rationale: El resumen es vago y carece de contexto claro.

### vi / comprehensibility / human label 1

- Item: `seahorse_test_vi_comprehensibility_016484_1shot`
- Scores: direct=4, target=2, pivot=1, bilingual=4
- Original summary: Chính quyền Bush đã đưa đội quân Cộng Hòa của Iran vào danh sách các tổ chức khủng bố.
- English pivot: The Bush administration placed Iran's Republican Guard on the list of terrorist organizations. The Bush administration placed Iran's Republican Guard on the list of terrorist organizations. [repetition conti...
- Target-rubric rationale: Câu văn có thể gây nhầm lẫn do thiếu ngữ cảnh và không rõ ràng về ý nghĩa của việc đưa quân vào danh sách tổ chức khủng bố.
- Pivot rationale: Repetition makes the summary unclear and difficult to understand.
- Bilingual rationale: Tóm tắt dễ hiểu và truyền đạt thông tin rõ ràng.

### vi / grammar / human label 1

- Item: `seahorse_test_vi_grammar_016479_1shot`
- Scores: direct=4, target=3, pivot=1, bilingual=4
- Original summary: Tàu tàng hình Ấn Độ thăm Hải Phòng
- English pivot: The Indian stealth ship visits Haiphong. The Indian stealth ship visits Haiphong. [repetition continues]
- Target-rubric rationale: Bản tóm tắt sử dụng ngữ pháp cơ bản đúng, nhưng có thể cải thiện về cấu trúc câu và sự mạch lạc.
- Pivot rationale: Repetition indicates poor grammar and lack of fluency.
- Bilingual rationale: Câu văn ngắn gọn, ngữ pháp đúng và dễ hiểu.

### es-ES / comprehensibility / human label 1

- Item: `seahorse_test_es-ES_comprehensibility_017125_1shot`
- Scores: direct=4, target=3, pivot=2, bilingual=4
- Original summary: El piercing de lóbulo es el más común. El piercing de cartílago es una opción moderna. El piercing de trago es un piercing avanzado. El piercing de caracola es un piercing común.
- English pivot: Lobe piercings are the most common. Cartilage piercings are a modern option. Tragus piercings are an advanced type. Conch piercings are a common type. [repetition continues]
- Target-rubric rationale: El resumen presenta información clara sobre diferentes tipos de piercings, pero la estructura es algo fragmentada, lo que puede dificulta...
- Pivot rationale: Repetitive structure affects overall clarity and engagement.
- Bilingual rationale: El resumen es claro y fácil de entender en general.

### es-ES / comprehensibility / human label 1

- Item: `seahorse_test_es-ES_comprehensibility_010058_mt5_small`
- Scores: direct=4, target=3, pivot=2, bilingual=4
- Original summary: El presidente de Argentina, Néstor y Cristina Fernández de Kirchner, se convirtieron en figuras importantes de la política argentina.
- English pivot: The president of Argentina, Néstor and Cristina Fernández de Kirchner, became important figures in Argentine politics. They became important figures in Argentine politics. [repetition continues]
- Target-rubric rationale: El resumen es comprensible, pero la mención de 'Néstor y Cristina Fernández de Kirchner' puede causar confusión, ya que no se aclara que...
- Pivot rationale: Repetition affects clarity and overall comprehensibility.
- Bilingual rationale: El resumen es claro y fácil de entender.
