// THUNK ALIAS -> sub_143865370 (jmp:0x1408ffbf0->0x143865370)
char __fastcall sub_143865370(__int64 a1, int a2)
{
  __int64 v2; // r8
  char result; // al
  __int64 v4; // r9
  unsigned __int64 v5; // r9
  unsigned __int64 v6; // r11
  __int64 v7; // r10

  v2 = *(_QWORD *)(a1 + 192);
  result = -1;
  v4 = *(_QWORD *)(a1 + 200) - v2;
  if ( v4 != 0 )
  {
    v5 = v4 >> 3;
    v6 = 0;
    do
    {
      v7 = *(_QWORD *)(*(_QWORD *)(v2 + 8 * v6) + 288LL);
      if ( v7 != 0 )
      {
        if ( *(_DWORD *)(v7 + 12) == a2 )
          return v6;
      }
      else if ( a2 == -1 )
      {
        return v6;
      }
      v6 = (unsigned __int8)(v6 + 1);
    }
    while ( v5 > v6 );
  }
  return result;
}
