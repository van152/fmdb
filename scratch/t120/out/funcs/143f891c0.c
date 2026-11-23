__int64 __fastcall sub_143F891C0(__int64 a1, _QWORD *a2, unsigned int a3, int a4, int a5, int a6, char a7, __int64 a8)
{
  __int64 v12; // rsi
  char v13; // bl
  __int64 v14; // rax
  __int64 v15; // rcx
  __int64 v16; // r15
  char v17; // r12
  __int64 v18; // rax
  __int64 v19; // rcx
  int v21; // [rsp+48h] [rbp-50h] BYREF
  __int64 v22; // [rsp+50h] [rbp-48h] BYREF
  char v23; // [rsp+58h] [rbp-40h]
  char v24; // [rsp+59h] [rbp-3Fh]

  if ( a7 != 0 )
  {
    sub_14121A480(a1: &v22);
    sub_140814B10(a1: *a2, a2: &v21, a3: a1 + 32);
    if ( v21 != 0 || (sub_140814B10(a1: *a2, a2: &v21, a3: a1 + 40), v21 != 0) )
    {
      v12 = qword_141B59FA0;
      if ( qword_141B59FA0 != 0 && v24 != 0 )
      {
        v13 = v23;
        v14 = (unsigned int)MEMORY[0x141947498]();
        v15 = *(_QWORD *)(v12 + 16);
        if ( v15 == 0 || v15 == (unsigned int)v14 )
        {
          if ( v13 == 0 )
            v14 = 0;
          *(_QWORD *)(v12 + 16) = v14;
        }
        *(_QWORD *)(v12 + 8) = v22;
      }
      return 0;
    }
    v16 = qword_141B59FA0;
    if ( qword_141B59FA0 != 0 && v24 != 0 )
    {
      v17 = v23;
      v18 = (unsigned int)MEMORY[0x141947498]();
      v19 = *(_QWORD *)(v16 + 16);
      if ( v19 == 0 || v19 == (unsigned int)v18 )
      {
        if ( v17 == 0 )
          v18 = 0;
        *(_QWORD *)(v16 + 16) = v18;
      }
      *(_QWORD *)(v16 + 8) = v22;
    }
  }
  if ( (_BYTE)a3 == 0 || (a3 = 0, (unsigned __int8)sub_141084540(a1, (_DWORD)a2, a3: 0, a4, a5, a6, a7, a8) != 0) )
    LOBYTE(a3) = 1;
  return a3;
}
