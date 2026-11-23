int *__fastcall sub_1411DF0C0(__int64 a1, int *a2, int a3, char a4, unsigned __int8 a5, __int64 a6)
{
  int v10; // edx
  int v11; // r9d
  int v12; // edi
  int v13; // eax
  int v14; // ebx
  int v15; // r8d
  int v16; // esi
  int v17; // r8d
  int v18; // r8d
  int v19; // r8d
  int v20; // r8d
  int v21; // r8d
  int v23; // edx
  char v24; // al
  int v25; // r8d
  int v26; // edx
  int v27; // ecx
  __int128 v28; // [rsp+50h] [rbp-68h] BYREF
  int v29; // [rsp+60h] [rbp-58h]
  char v30; // [rsp+64h] [rbp-54h]
  __int128 v31; // [rsp+70h] [rbp-48h] BYREF
  int v32; // [rsp+80h] [rbp-38h]
  char v33; // [rsp+84h] [rbp-34h]

  v31 = 0;
  v32 = 0;
  v33 = 1;
  if ( (_BYTE)word_141B60320 != 0 && (_BYTE)word_141B60460 == 6 )
  {
    v10 = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)qword_141B5FD40 + 40LL))(qword_141B5FD40, a1);
  }
  else
  {
    v10 = (unsigned __int16)word_141AB0260;
    if ( (unsigned __int16)word_141AB0260 >= 0x7E8u )
    {
      word_141AB0260 = 2023;
      LOWORD(v10) = 2023;
    }
  }
  if ( (unsigned __int8)sub_1411DCE60(a1, v10, a3, a5, (__int64)&v31, a4, a6, 0, 1, 0) == 0 )
  {
    if ( a5 != 0 )
    {
      if ( (_BYTE)a3 == 1 )
      {
        v28 = 0;
        v29 = 0;
        v30 = 1;
        if ( (_BYTE)word_141B60320 != 0 && (_BYTE)word_141B60460 == 6 )
        {
          v23 = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)qword_141B5FD40 + 40LL))(qword_141B5FD40, a1);
        }
        else
        {
          v23 = (unsigned __int16)word_141AB0260;
          if ( (unsigned __int16)word_141AB0260 >= 0x7E8u )
          {
            word_141AB0260 = 2023;
            LOWORD(v23) = 2023;
          }
        }
        LOBYTE(v11) = 1;
        v24 = sub_1411DCE60(a1, v23, 0, v11, (__int64)&v28, a4, 0, 0, 1, 0);
        v26 = -16777216;
        if ( DWORD1(v28) != 0 )
          v26 = DWORD1(v28);
        v27 = -16764768;
        if ( v24 != 0 )
          v27 = v26;
        LOBYTE(v25) = 3;
        if ( (unsigned __int8)sub_14150DD00(v27, -1, v25, 0, 0) != 0 )
        {
          *a2 = -16777216;
          return a2;
        }
      }
      else if ( (_BYTE)a3 == 0 )
      {
        *a2 = -16764768;
        return a2;
      }
      *a2 = -1;
      return a2;
    }
    v12 = *(_DWORD *)(4 * (*(int *)(a1 + 12) - 3 * ((*(int *)(a1 + 12) / 3uLL) & 0xFFFFFFFFFFFFFFFEuLL)) + 0x14188E760LL);
LABEL_16:
    LOBYTE(v11) = 2;
    sub_1411DF0C0(a1, (unsigned int)&v28, a3, v11, 1, 0);
    v14 = v28;
    if ( (unsigned __int8)sub_14150DD00(v28, v12, 0, 0, 0) != 0 )
    {
      v16 = -16744400;
      LOBYTE(v15) = 3;
      if ( (unsigned __int8)sub_14150DD00(v14, -16744400, v15, 0, 0) == 0 )
        goto LABEL_25;
      v16 = -4096;
      LOBYTE(v17) = 3;
      if ( (unsigned __int8)sub_14150DD00(v14, -4096, v17, 0, 0) == 0 )
        goto LABEL_25;
      v16 = -2097152;
      LOBYTE(v18) = 3;
      if ( (unsigned __int8)sub_14150DD00(v14, -2097152, v18, 0, 0) == 0 )
        goto LABEL_25;
      v16 = -1;
      LOBYTE(v19) = 3;
      if ( (unsigned __int8)sub_14150DD00(v14, -1, v19, 0, 0) == 0 )
        goto LABEL_25;
      v16 = -8388544;
      LOBYTE(v20) = 3;
      if ( (unsigned __int8)sub_14150DD00(v14, -8388544, v20, 0, 0) == 0 )
        goto LABEL_25;
      LOBYTE(v21) = 3;
      if ( (unsigned __int8)sub_14150DD00(v14, -16777216, v21, 0, 0) == 0 )
        v12 = -16777216;
    }
    v16 = v12;
LABEL_25:
    *a2 = v16;
    return a2;
  }
  v12 = DWORD1(v31);
  if ( a5 == 0 )
    goto LABEL_16;
  v13 = -16777216;
  if ( DWORD1(v31) != 0 )
    v13 = DWORD1(v31);
  *a2 = v13;
  return a2;
}
