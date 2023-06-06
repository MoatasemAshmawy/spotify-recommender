import Image from "next/image"

export interface songCardProps   {
    imageUrl: string,
    songName: string,
    songUrl: string,
    artistName: string,
    albumName: string,
}



const SongCard = ({imageUrl, songName, songUrl, artistName, albumName}:songCardProps) => {
  return (
    <a className="flex p-5 bg-white rounded-lg shadow-lg items-center justify-around w-full h-52 cursor-pointer hover:bg-gray-400 mb-5" href={songUrl} target="_blank">
        <Image alt={songName} src={imageUrl} width={200} height={200} className="rounded-full w-29 aspect-square object-cover" />
        <div className="flex flex-col items-center justify-center gap-3 text-black">
            <h1 className="text-xl font-bold">Listen Now</h1>
            <h1>{songName}</h1>
            <h2>{artistName}</h2>
            <h3>{albumName}</h3>
        </div>
    </a>
  )
}

export default SongCard