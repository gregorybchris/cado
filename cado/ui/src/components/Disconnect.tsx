interface DisconnectProps {
  image: any;
}

export default function Disconnect(props: DisconnectProps) {
  return (
    <div className="px-12">
      <div className="flex justify-center pt-10">
        <img src={props.image} alt="cado" width={300} />
      </div>
      <div className="mt-12 text-center">
        <div className="text-5xl">Ope!</div>
        <div className="mt-5 text-xl">We lost connection to the cado sever. Please check that it's still running!</div>
      </div>
    </div>
  );
}
