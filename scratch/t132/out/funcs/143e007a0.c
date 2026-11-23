__int64 __fastcall sub_143E007A0(__int64 a1, __int16 a2, char a3)
{
  __int64 result; // rax
  unsigned int v7; // eax
  unsigned int v8; // ecx

  result = sub_1400015E0();
  if ( a3 == 19 || (_BYTE)result != 0 )
  {
    *(_WORD *)(a1 + 168) = a2;
    v7 = sub_1411A3490(a1);
    v8 = 1;
    if ( (__int16)v7 >= 2 )
      v8 = v7;
    result = 10000;
    if ( (__int16)v8 < 10000 )
      result = v8;
    *(_WORD *)(a1 + 168) = result;
  }
  return result;
}
