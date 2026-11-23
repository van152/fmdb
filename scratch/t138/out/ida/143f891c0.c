__int64 __fastcall sub_143F891C0(__int64 a1, _QWORD *a2, unsigned int a3, int a4, int a5, int a6, char a7, __int64 a8)
{
  __int64 v12; // rcx
  __int64 v13; // rsi
  char v14; // bl
  __int64 v15; // rax
  __int64 v16; // rcx
  __int64 v17; // r15
  char v18; // r12
  __int64 v19; // rax
  __int64 v20; // rcx
  int v22; // [rsp+48h] [rbp-50h] BYREF
  __int64 v23; // [rsp+50h] [rbp-48h] BYREF
  char v24; // [rsp+58h] [rbp-40h]
  char v25; // [rsp+59h] [rbp-3Fh]

  if ( a7 != 0 )
  {
    sub_14121A480(a1: &v23);
    sub_140814B10(a1: *a2, a2: &v22, a3: a1 + 32);
    if ( v22 != 0 || (sub_140814B10(a1: *a2, a2: &v22, a3: a1 + 40), v22 != 0) )
    {
      v13 = qword_141B59FA0;
      if ( qword_141B59FA0 != 0 && v25 != 0 )
      {
        v14 = v24;
        v15 = (unsigned int)MEMORY[0x141947498](a1: v12);
        v16 = *(_QWORD *)(v13 + 16);
        if ( v16 == 0 || v16 == (unsigned int)v15 )
        {
          if ( v14 == 0 )
            v15 = 0;
          *(_QWORD *)(v13 + 16) = v15;
        }
        *(_QWORD *)(v13 + 8) = v23;
      }
      return 0;
    }
    v17 = qword_141B59FA0;
    if ( qword_141B59FA0 != 0 && v25 != 0 )
    {
      v18 = v24;
      v19 = (unsigned int)MEMORY[0x141947498](a1: v12);
      v20 = *(_QWORD *)(v17 + 16);
      if ( v20 == 0 || v20 == (unsigned int)v19 )
      {
        if ( v18 == 0 )
          v19 = 0;
        *(_QWORD *)(v17 + 16) = v19;
      }
      *(_QWORD *)(v17 + 8) = v23;
    }
  }
  if ( (_BYTE)a3 == 0 || (a3 = 0, (unsigned __int8)sub_141084540(a1, (_DWORD)a2, a3: 0, a4, a5, a6, a7, a8) != 0) )
    LOBYTE(a3) = 1;
  return a3;
}
