'use client'
import { signIn } from 'next-auth/react'
import spotify from '../../public/spotify.svg'
import Image from 'next/image'

export default function Home() {
  return (
    <main className="flex flex-col h-screen justify-center items-center">
      <h1 className='text-4xl'>Spotify Recommender</h1>
      <button className=" flex justify-center items-center bg-green-500 text-white px-4 py-2 rounded-md mt-5" onClick={() => {signIn('spotify',{callbackUrl:'/recommendations'})}}>
        <Image src={spotify} alt="Spotify" className='h-8 w-8 mr-2'/>
        Sign In With Spotify
      </button>
    </main>
  )
}
