__int64 __fastcall sub_1415D5110(__int64 a1, __int64 *a2, char a3, __int64 a4, int a5, int a6, char a7, __int64 a8)
{
  unsigned int v8; // ebp
  __int64 v11; // rbx
  int v13; // [rsp+30h] [rbp-58h]

  if ( a3 == 0
    || (v11 = a1 + -*(_DWORD *)(a1 - 4),
        v8 = 0,
        (unsigned __int8)sub_140E06EC0(a1: v11 - 240, a2, a3: 0, a4, a5, a6, a7, a8) != 0)
    && (v8 = 0, (unsigned __int8)sub_140DC1D30(a1: v11, a2, a3: 0, a4, a5, a6, a7, a8) != 0)
    && (v8 = 0, (unsigned __int8)sub_140DD8520(a1: (int)v11 + 376, (_DWORD)a2, a3: 0, a4, a5, a6, a7, a8) != 0)
    && (v8 = 0, (unsigned __int8)sub_140DFB5C0(a1: (int)v11 + 160, (_DWORD)a2, a3: 0, a4, a5, a6, a7, a8) != 0)
    && (LOBYTE(v13) = a7,
        v8 = 0,
        (unsigned __int8)sub_141084540(a1: v11, (_DWORD)a2, a3: 0, a4, a5, a6, a7: v13, a8) != 0) )
  {
    LOBYTE(v8) = 1;
  }
  return v8;
}
