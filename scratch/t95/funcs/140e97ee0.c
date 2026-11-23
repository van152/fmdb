// THUNK ALIAS -> sub_143C5AAE0 (jmp:0x140e97ee0->0x143c5aae0)
__int64 __fastcall sub_143C5AAE0(_QWORD *a1, __int64 a2)
{
  __int64 v3; // rsi
  __int64 v5; // rdi
  unsigned int v6; // ebx
  unsigned __int64 v7; // rcx
  __int64 v8; // rdi
  __int64 v9; // rdi
  __int128 v11; // [rsp+20h] [rbp-48h] BYREF
  __int64 v12; // [rsp+30h] [rbp-38h]
  __int128 *v13; // [rsp+40h] [rbp-28h] BYREF

  v11 = 0;
  v12 = 0;
  v3 = a1[1] - *a1;
  if ( v3 != 0 )
  {
    if ( v3 < 0 )
      sub_1400526C0(a1);
    *(_QWORD *)&v11 = sub_1407E4490(qword_141ABD470, v3);
    v12 = v11 + 8 * (v3 >> 3);
    v5 = a1[1] - *a1;
    sub_141758A00();
    *((_QWORD *)&v11 + 1) = v11 + v5;
  }
  v13 = &v11;
  v6 = sub_140EB5160(&v13, a2);
  if ( (_QWORD)v11 != 0 )
  {
    v7 = v12 - v11;
    if ( v12 - (_QWORD)v11 == -1 )
    {
      v7 = *(unsigned int *)(v11 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_14:
        MEMORY[0x141948990](v11 - *(unsigned int *)(qword_141ABD470 + 48));
        return v6;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_14;
    }
    v8 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v8) >> 3 <= v7 )
      goto LABEL_14;
    v9 = *(_QWORD *)(v8 + 8 * v7);
    if ( v9 == 0 )
      goto LABEL_14;
    MEMORY[0x1419475D8](v9 + 32, v11 - *(unsigned int *)(v9 + 120));
    if ( (*(_BYTE *)(v9 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v9 + 64)) == 0)
      && *(_BYTE *)(v9 + 97) != 0 )
    {
      sub_1412D33C0(v9);
    }
  }
  return v6;
}
