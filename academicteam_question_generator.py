#!/usr/bin/env python3
# pylint: disable=C0303,C0301
"""
Enhanced Academic Team Question Generator

This script generates a PDF document from a provided set of questions.
These questions are in tossup and sixty-second formats.

Required packages:
pip install reportlab

Usage:
python academicteam_question_generator.py
python academicteam_question_generator.py --questions /path/to/db.db
"""

import argparse
import csv
import random
from datetime import datetime

# PDF imports
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

class AcademicTeamQuestionGenerator:
    """Class to represent all functions and data for generating the KofC database"""

    def __init__(self, data_path="ok_knights_directory.db"):
        self.data_path = data_path
        self.pdf_story = []
        self.pdf_styles = getSampleStyleSheet()
        self.setup_pdf_styles()

    def setup_pdf_styles(self):
        """Setup custom PDF styles"""
        self.pdf_styles.add(ParagraphStyle(
            name='SmallItalicTitle',
            parent=self.pdf_styles['Title'],
            fontSize=16,
            spaceAfter=40,
            spaceBefore=80,
            alignment=TA_CENTER,
            textColor=colors.black,
            fontName='Times-Italic'
        ))
        
        self.pdf_styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.pdf_styles['Title'],
            fontSize=28,
            spaceAfter=20,
            spaceBefore=20,
            alignment=TA_CENTER,
            textColor=colors.black,
            fontName='Times-Roman'
        ))

        # Answer Style
        self.pdf_styles.add(ParagraphStyle(
            name='AnswerStyle',
            parent=self.pdf_styles['Normal'],
            leftIndent=20
        ))

        # Center style
        self.pdf_styles.add(ParagraphStyle(
            name='CenterNormal',
            parent=self.pdf_styles['Normal'],
            alignment=TA_CENTER,
            fontSize=10
        ))

        # Right style
        self.pdf_styles.add(ParagraphStyle(
            name='RightNormal',
            parent=self.pdf_styles['Normal'],
            alignment=TA_RIGHT,
            fontSize=10
        ))

        # Left Style
        self.pdf_styles.add(ParagraphStyle(
            name='LeftNormal',
            parent=self.pdf_styles['Normal'],
            alignment=TA_LEFT,
            fontSize=9,
            fontName='Times-Roman'
        ))

        self.pdf_styles.add(ParagraphStyle(
            name='CategoryTitle',
            parent=self.pdf_styles['Normal'],            
            alignment=TA_CENTER,
            fontName="Times-Bold",
            fontSize=12
        ))

        # Bold Style
        self.pdf_styles.add(ParagraphStyle(
            name='BoldNormal',
            parent=self.pdf_styles['CategoryTitle'],
            alignment=TA_LEFT,
            fontSize=10,
        ))

    def create_title_page(self, grades='5&6', tournament_type='Practice Questions', year='2025-2026', game_number='1'):
        """Create the title page for the game document."""
        title_elements = []

        # Add main title
        title_elements.append(Paragraph("Saint John Nepomuk Academic Team", self.pdf_styles['SmallItalicTitle']))
        title_elements.append(Paragraph(f"Grades {grades}", self.pdf_styles['CustomTitle']))
        title_elements.append(Paragraph(f"{tournament_type}", self.pdf_styles['CustomTitle']))
        title_elements.append(Paragraph("Questions", self.pdf_styles['CustomTitle']))
        title_elements.append(Paragraph(f"{year}", self.pdf_styles['CustomTitle']))
        title_elements.append(Spacer(width=0, height=80))
        title_elements.append(Paragraph(f"Game {game_number}", self.pdf_styles['CustomTitle']))
        
        # Add page break after title page
        title_elements.append(PageBreak())
        
        return title_elements

    def create_tossup_round(self, question_number, question_data):
        """Create a PDF table for tossup questions"""
        data = [
            # Row 1: Role (spanning all columns)
            [
                Paragraph(question_number, self.pdf_styles["Normal"]),
                Paragraph(question_data['q'], self.pdf_styles['Normal'])
            ],
            # Row 2: Details
            [
                Paragraph("", self.pdf_styles['Normal']),
                Paragraph(question_data['a'], self.pdf_styles['AnswerStyle']),
            ]
        ]
        
        table = Table(
            data,
            colWidths=[0.4*inch, 6.6*inch],
            rowHeights=[None, None])
        
        # Table styling (no borders)
        table.setStyle(TableStyle([
        #     ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        #     ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        #     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        #     ('FONTSIZE', (0, 0), (-1, 0), 12),
        #     ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        #     ('TOPPADDING', (0, 0), (-1, 0), 5),
        #     ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        return KeepTogether(table)
    
    def create_sixtysecond_round(self, round_data):
        """A"""
        # Create title
        title = round_data['title']
        instruct = round_data['instruct']
        questions = round_data['questions']

        elements = []
        elements.append(Paragraph(title, self.pdf_styles['CategoryTitle']))
        elements.append(Spacer(0, 4))
        elements.append(Paragraph(instruct, self.pdf_styles['LeftNormal']))        
        elements.append(Spacer(0, 2))

        data = []
        data.append([Paragraph(''), Paragraph(''), Paragraph('')])
        for i, question in enumerate(questions):
            if i == 10:
                data.append([Paragraph('EXTRA:', self.pdf_styles['BoldNormal']), Paragraph(''), Paragraph('')])

            data.append([
                Paragraph(str(i+1), self.pdf_styles['LeftNormal']),
                Paragraph(question['q'], self.pdf_styles['LeftNormal']),
                Paragraph(question['a'], self.pdf_styles['LeftNormal'])
            ])

        table = Table(
            data,
            #colWidths=[0.4*inch, 2.0*inch, 3.6*inch],
            colWidths=[0.4*inch, None, None],
            rowHeights=[0.15*inch for _ in data]
        )

        # Table styling (no borders)
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('SPAN', (0, 11), (1, 11)),
        ]))

        elements.append(KeepTogether(table))

        return elements

    def get_sample_data(self):
        """Sample data for testing"""
        return [
            {"q": "Name the four blood types.", "a": "A, B, AB, O"},
            {"q": "Name the state located immediately west of Alabama.", "a": "Mississippi"}
        ]
    
    def get_sample_data2(self):
        """Sample data for testing"""
        return {
        'title': 'U.S. Presidents by Century',
        'instruct': "During what century was each of the following U.S. Presidents in Office? For example, George H. W. Bush was in office during the 20th century.",
        'questions': [
                {'q': 'Theodore Roosevelt', 'a': "20th"},
                {'q': 'James Buchanan', 'a': '19th'},
                {'q': 'Theodore Roosevelt', 'a': "20th"},
                {'q': 'James Buchanan', 'a': '19th'},
                {'q': 'Theodore Roosevelt', 'a': "20th"},
                {'q': 'James Buchanan', 'a': '19th'},
                {'q': 'Theodore Roosevelt', 'a': "20th"},
                {'q': 'James Buchanan', 'a': '19th'},
                {'q': 'Theodore Roosevelt', 'a': "20th"},
                {'q': 'James Buchanan', 'a': '19th'},
                {'q': 'Bill Clinton', 'a': '20th'}
            ]
        }
    
    def get_tossup_question_data(self, num_questions=20, filename='./sample_questions.txt'):
        """Randomly samples from the questions file 20 questions"""
        data = []
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
            for row in reader:
                data.append(
                    {
                        'q': row[0],
                        'a': row[1],
                        'category': row[2],
                        'grade': row[3]
                    }
                )

        rng = random.Random(12345)
        sample_size = num_questions
        return rng.sample(data, sample_size)


    def generate_document(self, output_base, num_tossup=20):
        """Generate PDF document with simple linked TOC"""
        print("Generating PDF document with simple TOC...")
        
        margin_factor = 1.0

        # Generate PDF document with timestamp        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"{output_base}_{timestamp}.pdf"

        doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                            rightMargin=margin_factor*inch, leftMargin=margin_factor*inch,
                            topMargin=margin_factor*inch, bottomMargin=margin_factor*inch)
        
        story = []
        
        # Add title page
        story.extend(self.create_title_page())
        
        # tossup section with anchor
        questions = self.get_tossup_question_data(num_questions=num_tossup)
        if questions:
            for n, question in enumerate(questions):
                print(f"Writing question {n+1}")
                story.append(self.create_tossup_round(f"{n+1}", question))
                story.append(Spacer(1, 15))
            
        story.append(PageBreak())

        # sixty-second section with anchor
        # data = self.get_sample_data2()

        # story.extend(self.create_sixtysecond_round(data))
        # story.append(Spacer(width=0, height=10))

        # story.extend(self.create_sixtysecond_round(data))
        # story.append(Spacer(width=0, height=10))

        # story.extend(self.create_sixtysecond_round(data))
        # story.append(PageBreak())

        doc.build(story)
        print(f"PDF document saved as: {pdf_filename}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Academic Team Game Generator')
    parser.add_argument('--questions', default='sample_questions.txt',
                       help='questions file path')
    parser.add_argument('--output', default='Questions',
                       help='Output filename base')
    
    parser.add_argument('--num_tossup', default='80', help='number of tossups to generate')
    
    args = parser.parse_args()
    
    generator = AcademicTeamQuestionGenerator(args.questions)
    generator.generate_document(args.output, int(args.num_tossup))
    
    print("\nSuccess! Directory generated as PDF")

if __name__ == "__main__":
    main()
