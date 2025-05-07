quran_html_template_start = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Al-Quran {{surat_name}} -- Abjad-e-Qamari -- Faiz-e-Hussaini</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Scheherazade+New:wght@400;700&display=swap');
        
        :root {
            --primary-color: #26572a;
            --secondary-color: #cb8d38;
            --verse-bg: #f9f6f0;
            --border-color: goldenrod;
            --text-color: #2d2d2d;
            --header-color: #1f4224;
            --qamari-color: #26572a;
            --table-header-bg: #e6dac8;
            --table-border: #d4c4a8;
            --batini-color: #8b6b29; /* A deeper gold/bronze tone */
            --malfuzi-color: #4e5a34; /* A muted olive green that complements the primary green */

        }
        
        body {
            font-family: 'Scheherazade New', 'Amiri', 'Traditional Arabic', serif;
            margin: 2px;
            background-color: #f5f0e6;
            color: var(--text-color);
            direction: rtl;
            font-size: 30px;
            line-height: 1.6;
        }

        .calculation {
            font-size: 24px;
            overflow: auto;
        }

        /* Ayah marker styles */
        .ayah-marker {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 35px;
            height: 35px;
            color: #26572a;
            font-family: "Traditional Arabic", "Amiri", Arial, sans-serif;
            font-size: 20px;
            margin: 0 5px;
            position: relative;
        }

        /* Optional: decorative accent */
        .ayah-marker::before {
            content: "۝";
            position: absolute;
            font-size: 36px;
            opacity: 1;
            bottom: -10px;
            color: #cb8d38;
        }
        
        .container {
            max-width: 1020px;
            margin: 0 auto;
            background-color: #fff;
            /*padding: 2px;*/
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            border-radius: 10px;
            /*border: 2px solid var(--border-color);*/
        }
        
        h1, h2, h3 {
            color: var(--primary-color);
            text-align: center;
            font-family: 'Amiri', 'Traditional Arabic', serif;
        }
        
        h1 {
            font-size: 42px;
            margin-bottom: 10px;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 10px;
        }
        
        h2 {
            font-size: 36px;
            color: var(--secondary-color);
        }
        
        .verse-section {
            margin-bottom: 40px;
            padding: 20px;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            background-color: var(--verse-bg);
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            position: relative;
        }
        
        .verse-section::after {
            content: "";
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 80%;
            height: 1px;
            background: linear-gradient(to right, transparent, var(--border-color), transparent);
        }
        
        .arabic-text {
            font-size: 38px;
            background-color: rgba(255, 255, 255, 0.7);
            padding: 15px;
            text-align: center;
            letter-spacing: 1px;
            border-radius: 5px;
            box-shadow: inset 0 0 5px rgba(0,0,0,0.1);
            font-family: 'Scheherazade New', serif;
            border: 1px solid var(--border-color);
            line-height: 1.8;
        }
        
        .total-value {
            font-size: 36px;
            background-color: rgba(255, 255, 255, 0.7);
            padding: 2px 15px;
            font-weight: bold;
            color: var(--primary-color);
            border-radius: 5px;
            margin: 2px 0;
            display: inline-block;
        }
        
        .total-malfuzi-span {
            color: var(--malfuzi-color);
        }
        
        .grand-total {
            text-align: center;
            margin-top: 40px;
            padding: 25px;
            background-color: var(--verse-bg);
            border-radius: 10px;
            font-size: 1.3em;
            border: 2px solid var(--border-color);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .qamari-grand-total {
            background-color: rgba(38, 87, 42, 0.08);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border: 1px solid var(--primary-color);
            color: var(--primary-color);
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }

        .batini-grand-total {
            background-color: rgba(203, 141, 56, 0.08);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border: 1px solid var(--batini-color);
            color: var(--batini-color);
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }

        .malfuzi-grand-total {
            margin-top: 15px;
            background-color: rgba(78, 90, 52, 0.08);
            border-radius: 8px;
            padding: 15px;
            border: 1px solid var(--malfuzi-color);
            color: var(--malfuzi-color);
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }
        
        .right-to-left {
            text-align: center;
        }
        
        .left-to-right {
            text-align: center;
            letter-spacing: 1px;
            direction: ltr;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0px 0;
            direction: rtl;
            background-color: #fff;
            border: 1px solid var(--border-color);
            border-radius: 5px;
            overflow: auto;
        }
        
        .translations p, .translations div {
            padding: 15px;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            margin: auto;
            background-color: rgba(255, 255, 255, 0.7);
        }

        .light-letter-left-border {
            border-left-color: #e9e9e9;
        }

        .dark-letter-left-border {
            border-left-color: var(--table-border);
        }
        
        th, td {
            padding: 8px 4px;
            border: 1px solid var(--table-border);
            text-align: center;
        }
        
        th {
            background-color: var(--table-header-bg);
            color: var(--header-color);
            font-weight: bold;
        }
        
        .qamari-malfuzi-table {
            margin-bottom: 30px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        }
        
        .letter-row {
            font-weight: bold;
            background-color: rgba(255, 255, 255, 0.9);
            letter-spacing: 1px;
        }
        
        .value-row {
            background-color: rgba(242, 238, 226, 0.7);
        }
        
        .letter-value-row td {
            padding: 0 2px !important;
        }

        .malfuzi-value-row {
            background-color: #cb8d380f;
            font-style: oblique;
            color: gray;
        }
        
        .qamari-value-row {
            color: #700000;
        }

        .word-analysis {
            margin-top: 30px;
            padding: 20px;
            background-color: var(--verse-bg);
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }
        
        .word-item {
            display: inline-block;
            margin: 10px;
            padding: 12px;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            background-color: #fff;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        
        .word-text {
            font-size: 28px;
            font-weight: bold;
        }
        
        .word-value {
            color: var(--primary-color);
            font-weight: bold;
        }

        

        .total-qamari-span,
        .total-bayenati-span,
        .total-malfuzi-span {
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            text-align: center;
        }
        
        .translations {
            background-color: rgba(249, 246, 240, 0.7);
            border-radius: 8px;
            font-size: 26px;
            padding: 2px;
            margin-top: 10px;
            border: 1px solid var(--border-color);
        }
        .adad-row {
            display: flex;
            flex-direction: row-reverse;
            justify-content: space-between;
            align-items: center;
            position: relative;
            direction: rtl;
            overflow: auto;
        }
        .translation-title {
            color: var(--header-color);
            position: absolute;
            margin-top: -28px;
            left: 50%;
            transform: translateX(-50%);
            background-color: white;
            padding: 0px 10px;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            font-size: 12px;
            z-index: 1;
            width: max-content;
        }
        
        /* Decorative Elements */
        .surah_header {
            position: relative;
            /*padding-top: 30px;*/
            margin-bottom: 8px;
            border: 2px solid var(--border-color);
        }
        
        .surah_header::before,
        .surah_header::after {
            content: "۩";
            font-size: 32px;
            color: var(--secondary-color);
            position: absolute;
            top: 0;
        }
        
        .surah_header::before {
            right: 20px;
        }
        
        .surah_header::after {
            left: 20px;
        }

        .letter-value-row{
            font-size: 8px;
        }

        
        
        /* Print-specific styles */
        @media print {
            body {
                background-color: white;
                margin: 0;
                padding: 0;
                font-size: 12pt;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                color-adjust: exact !important;
            }
            
            .container {
                max-width: 100%;
                margin: 0;
                padding: 2px;
                box-shadow: none;
                /* border: none; */
            }
            
            h1 {
                font-size: 24pt;
                margin-bottom: 10px;
            }
            
            h2 {
                font-size: 36px;
                color: var(--secondary-color);
            }

            .surah_header {
                position: relative;
                /* padding-top: 20px;*/
                margin-bottom: 8px;
                border: 2px solid var(--border-color);
            }
            
            .verse-section {
                page-break-inside: avoid;
                break-inside: avoid;
                margin-bottom: 30px;
                padding: 15px;
                border: 2px solid var(--border-color);
            }
            
            .arabic-text {
                font-size: 20pt;
                padding: 10px;
            }
            
            .total-value {
                font-size: 18pt;
                padding: 5px 10px;
            }
            
            table {
                page-break-inside: avoid;
                break-inside: avoid;
                font-size: 12pt;
            }
            
            th, td {
                padding: 8px;
            }
            
            .grand-total {
                page-break-before: always;
                break-before: page;
                font-size: 20pt;
                padding: 20px;
                margin-top: 20px;
            }
            
            .word-item {
                padding: 8px;
                margin: 5px;
            }
            
            .word-text {
                font-size: 16pt;
            }
            
            .translations {
                font-size: 14pt;
                padding: 2px;
                margin-top: 0px;
            }
            
            
            
            
            .total-value,
            .total-malfuzi-span {
                background-color: transparent !important;
                color: #000 !important;
            }
            
            /* Fix for page breaks */
            .verse-section:last-of-type {
                page-break-after: avoid;
                break-after: avoid;
            }
        }
    </style>
</head>
<body>
    <div class="surah_header container">
        <h1>{{surat_name}}</h1>
        <h2>{{bismillah}}</h2>
    </div>
    <div class="container">
"""
