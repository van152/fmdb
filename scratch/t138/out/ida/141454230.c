char __fastcall sub_141454230(__int16 a1, char a2)
{
  char result; // al

  result = 1;
  switch ( a2 )
  {
    case 3:
      return result;
    case 4:
      result = 2;
      if ( a1 == 74 )
        result = 9;
      if ( a1 == 5 )
        result = 9;
      break;
    case 19:
      result = 3;
      break;
    case 39:
      result = 4;
      break;
    case 40:
      result = 5;
      break;
    default:
      result = 0;
      break;
  }
  return result;
}
