__int64 __fastcall sub_14452D790(__int64 a1, _QWORD *a2, __int64 a3, int a4, int a5, int a6, char a7, __int64 a8)
{
  __int64 v11; // rsi
  __int64 v12; // rsi
  unsigned int v13; // esi
  __int64 v14; // rdi
  char v15; // bl
  __int64 v16; // rax
  __int64 v17; // rcx
  int v19; // [rsp+40h] [rbp-38h] BYREF
  __int64 v20; // [rsp+48h] [rbp-30h] BYREF
  char v21; // [rsp+50h] [rbp-28h]
  char v22; // [rsp+51h] [rbp-27h]

  sub_14121A480(&v20);
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 24, 4);
  if ( *(_DWORD *)(v11 + 16) != 0
    || (v12 = *a2,
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 64, 4),
        *(_DWORD *)(v12 + 16) != 0)
    || (sub_140814B10(*a2, &v19, a1 + 32), v19 != 0)
    || (sub_140814B10(*a2, &v19, a1 + 40), v19 != 0)
    || (sub_140814B10(*a2, &v19, a1 + 48), v19 != 0)
    || (unsigned __int8)sub_140DB8980(a1 + 56, a2) == 0
    || (sub_14157E7B0(&v19, a2, a1 + 72), v19 != 0) )
  {
    v13 = 0;
  }
  else
  {
    v13 = sub_140FAED40(a1, (_DWORD)a2, 0, a4, a5, a6, a7, a8);
  }
  v14 = qword_141B59FA0;
  if ( qword_141B59FA0 != 0 && v22 != 0 )
  {
    v15 = v21;
    v16 = (unsigned int)MEMORY[0x141947498]();
    v17 = *(_QWORD *)(v14 + 16);
    if ( v17 == 0 || v17 == (unsigned int)v16 )
    {
      if ( v15 == 0 )
        v16 = 0;
      *(_QWORD *)(v14 + 16) = v16;
    }
    *(_QWORD *)(v14 + 8) = v20;
  }
  return v13;
}
