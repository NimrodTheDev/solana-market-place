import React, { useState } from 'react'
import { Upload, ArrowRight } from 'lucide-react';

// import Hero from '../components/landingPage/hero'

function CreateCoin() {
    const [preview, setPreview] = useState<string | null>(null);

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file && file.type.startsWith('image/')) {
            setPreview(URL.createObjectURL(file));
        }
    };
    return (
        <div className='relative'>
            <div className="h-64 z-10 crtGradient background-container  top-10 left-10  ...">
                <div className="h-40  justify-center...">
                    <div className="flex flex-col items-center justify-center h-full">
                        <h1 className="text-5xl font-bold text-custom-dark-blue mb-4 text-center">Launch a new Project</h1>
                        <p className="text-gray-800 max-w-lg mx-auto text-center">
                        Build your reputation in the Web3 ecosystem as you bring your vision to life on Notty Terminal.
                        </p>
                    </div>
                </div>
            </div>

            <div className="h-[calc(100vh+10rem)] bg-custom-dark-blue "></div>
            <div className="flex justify-center items-center mt-10  absolute left-16 right-16 border-gray-600 border  top-36 h-218 bg-custom-dark-blue z-10 p-4 text-white rounded p-10">
                {/* <article className="flex  justify-self-end self-start">lwa</article> */}
                <form method='POST' className="flex flex-col justify-center w-96 mb-10 mt=10">
                    <div className="mb-8">
                        <h1 className="text-2xl font-bold mb-2">Project details</h1>
                        <p className="text-gray-400">Provide important details about your project</p>
                    </div>
                    <div className="space-y-6">
                        <div>
                            <label htmlFor="projectName" className='block text-sm font-medium mb-2'>Project name</label>
                            <input type="text" name="" id="projectName" className="w-full bg-gray-800 border border-gray-700 rounded px-4 py-2 text-white no-background" placeholder="Enter your project name" />
                        </div>
                        <div>
                            <label className="block text-sm font-medium mb-2" htmlFor="projectDesc">Project description</label>
                            <input type="text" name="" id="projectDesc" className="w-full bg-gray-800 border border-gray-700 rounded px-4 py-2 text-white no-background" placeholder="Describe your projects" />
                        </div>
                        <div>
                            <label htmlFor="image" className="block text-sm font-medium mb-2">Image</label>
                            {/* <div className="">
                                <input type="file"
                                    accept="image/*"
                                    onChange={handleImageChange}
                                    className="mt-5"
                                    id="image" />
                            </div> */}
                                <div className="flex flex-col items-center justify-center h-40 bg-gray-800 border border-gray-700 rounded p-4">
                                    {preview ? (
                                        <div className="w-full h-full relative">
                                            <img 
                                                src={preview} 
                                                alt="Project preview" 
                                                className="w-full h-full object-contain"
                                            />
                                            <button 
                                                type="button" 
                                                className="absolute top-2 right-2 bg-gray-700 p-1 rounded-full"
                                                onClick={() => setPreview(null)}
                                            >
                                                ✕
                                            </button>
                                        </div>
                                    ) : (
                                        <>
                                            <Upload className="text-gray-400 mb-2" size={24} />
                                            <p className="text-gray-400 text-sm mb-4">Drag and drop an image</p>
                                            <label htmlFor="file-upload" className="cursor-pointer px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-md text-sm">
                                                Select file
                                            </label>
                                            <input 
                                                id="file-upload" 
                                                type="file" 
                                                accept="image/*" 
                                                onChange={handleImageChange} 
                                                className="hidden"
                                            />
                                        </>
                                    )}
                                </div>
                        </div>
                        <div>
                            <label htmlFor="webAddress" className="block text-sm font-medium mb-2">Website Address</label>
                            <input type="text" name="" id="webAddress" className="w-full bg-gray-800 border border-gray-700 rounded px-4 py-2 text-white no-background" placeholder="Add website Address" />
                        </div>
                        <div>
                            <label htmlFor="twithand" className="block text-sm font-medium mb-2">Twitter Handle</label>
                            <input type="text" name="" id="twithand" className="w-full bg-gray-800 border border-gray-700 rounded px-4 py-2 text-white no-background" placeholder="Add your twitter handle" />
                        </div>
                        <div>
                            <label htmlFor="discord" className="block text-sm font-medium mb-2">Discord Channel</label>
                            <input type="text" name="" id="discord" className="w-full bg-gray-800 border border-gray-700 rounded px-4 py-2 text-white no-background" placeholder="Add your discord address" />
                        </div>
                    </div>
                    <div className="flex justify-start mt-8">
                        <button
                            type="submit"
                            className="flex items-center justify-center bg-custom-light-purple hover:bg-indigo-600 text-white px-6 py-2 rounded transition-colors"
                        >
                            Preview
                            <ArrowRight className="ml-2 h-4 w-4" />
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default CreateCoin