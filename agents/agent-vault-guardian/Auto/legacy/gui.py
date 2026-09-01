"""
Document Classifier GUI
GUI component module
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
import importlib.util

# Add the current directory to the path to import classifier
spec = importlib.util.spec_from_file_location("classifier", os.path.join(os.path.dirname(__file__), "classifier.py"))
classifier_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(classifier_module)
DocumentClassifier = classifier_module.DocumentClassifier


class DocumentClassifierGUI:
    def __init__(self, parent):
        self.parent = parent
        self.classifier = DocumentClassifier()

        # Initialize variables
        self.selected_files = []
        self.results = {}

        self.create_widgets()

    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.parent, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for resizing
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Document Classifier", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="Select Documents", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)

        self.file_listbox = tk.Listbox(file_frame, height=6)
        self.file_listbox.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        select_button = ttk.Button(file_frame, text="Browse Files", command=self.browse_files)
        select_button.grid(row=1, column=0, padx=(0, 5))

        clear_button = ttk.Button(file_frame, text="Clear List", command=self.clear_file_list)
        clear_button.grid(row=1, column=1, padx=(5, 0))

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Classification Results", padding="10")
        results_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Classify button
        classify_button = ttk.Button(main_frame, text="Classify Documents", command=self.start_classification)
        classify_button.grid(row=4, column=0, columnspan=3, pady=(20, 0))

    def browse_files(self):
        """Open file dialog to select PDF files"""
        file_types = [("PDF files", "*.pdf"), ("All files", "*.*")]
        filenames = filedialog.askopenfilenames(title="Select documents to classify", filetypes=file_types)

        for filename in filenames:
            if filename not in self.selected_files:
                self.selected_files.append(filename)
                self.file_listbox.insert(tk.END, os.path.basename(filename))

    def clear_file_list(self):
        """Clear the selected files list"""
        self.selected_files = []
        self.file_listbox.delete(0, tk.END)
        self.results_text.delete(1.0, tk.END)

    def start_classification(self):
        """Start the classification process in a separate thread"""
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select at least one document to classify.")
            return

        # Disable the classify button during processing
        for child in self.parent.winfo_children():
            for widget in child.winfo_children():
                if isinstance(widget, ttk.Button) and "Classify" in str(widget.cget("text")):
                    widget.config(state="disabled")

        # Start classification in a separate thread
        classification_thread = threading.Thread(target=self.classify_documents)
        classification_thread.daemon = True
        classification_thread.start()

    def classify_documents(self):
        """Classify the selected documents"""
        # Update GUI in the main thread
        self.parent.after(0, self.progress.start)
        self.parent.after(0, lambda: self.results_text.delete(1.0, tk.END))
        self.parent.after(0, lambda: self.results_text.insert(tk.END, "Starting classification...\n"))

        for i, filepath in enumerate(self.selected_files):
            try:
                # Update GUI in the main thread
                self.parent.after(0, lambda x=i, total=len(self.selected_files):
                                 self.results_text.insert(tk.END, f"\nProcessing ({x+1}/{total}): {os.path.basename(filepath)}\n"))

                # Perform classification
                classification_result = self.classifier.classify_document(filepath)

                # Store result
                self.results[filepath] = classification_result

                # Update GUI in the main thread
                self.parent.after(0, lambda result=classification_result, fname=os.path.basename(filepath):
                                 self.results_text.insert(tk.END, f"Category: {result}\n"))

            except Exception as e:
                error_msg = f"Error processing {os.path.basename(filepath)}: {str(e)}"
                self.parent.after(0, lambda msg=error_msg:
                                 self.results_text.insert(tk.END, f"{msg}\n"))

        # Finalize GUI updates in the main thread
        self.parent.after(0, self.progress.stop)
        self.parent.after(0, lambda: self.results_text.insert(tk.END, "\nClassification complete!"))

        # Re-enable the classify button
        for child in self.parent.winfo_children():
            for widget in child.winfo_children():
                if isinstance(widget, ttk.Button) and "Classify" in str(widget.cget("text")):
                    self.parent.after(0, lambda w=widget: w.config(state="enabled"))


if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentClassifierGUI(root)
    root.mainloop()