// THUNK ALIAS -> sub_144017DE0 (jmp:0x1411de560->0x144017de0)
int *__fastcall sub_144017DE0(__int64 a1, int *a2)
{
  __int64 v4; // rdi
  int v5; // r9d
  __int64 v6; // rax
  int v7; // ecx
  int v8; // edx
  __int128 v10; // [rsp+50h] [rbp-28h] BYREF
  int v11; // [rsp+60h] [rbp-18h]
  char v12; // [rsp+64h] [rbp-14h]

  do
  {
    v4 = a1;
    if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 32LL))(qword_141B5AD60) != 0 )
      break;
    if ( *(_BYTE *)(v4 + 186) != 0 )
      break;
    a1 = sub_140E75FF0(v4, 0);
    if ( a1 == 0 )
      break;
  }
  while ( a1 != v4 );
  v6 = *(_QWORD *)(v4 + 176);
  if ( v6 == 0 || (v7 = *(_DWORD *)(v6 + 168)) == 0 || v7 == *(_DWORD *)(v6 + 160) )
  {
    v10 = 0;
    v11 = 0;
    v12 = 1;
    if ( (_BYTE)word_141B60320 != 0 && (_BYTE)word_141B60460 == 6 )
    {
      v8 = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)qword_141B5FD40 + 40LL))(qword_141B5FD40, v4);
    }
    else
    {
      v8 = (unsigned __int16)word_141AB0260;
      if ( (unsigned __int16)word_141AB0260 >= 0x7E8u )
      {
        word_141AB0260 = 2023;
        LOWORD(v8) = 2023;
      }
    }
    LOBYTE(v5) = 1;
    if ( (unsigned __int8)sub_1411DCE60(v4, v8, 0, v5, (__int64)&v10, 3, 0, 0, 1, 0) == 0 )
    {
      *a2 = -16764768;
      return a2;
    }
    v7 = -16777216;
    if ( DWORD1(v10) != 0 )
      v7 = DWORD1(v10);
  }
  *a2 = v7;
  return a2;
}
