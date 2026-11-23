char __fastcall sub_143ECD5C0(__int64 a1, __int64 a2, __int64 **a3)
{
  unsigned int v4; // edi
  __int64 v6; // rcx

  v4 = a2;
  if ( (unsigned __int8)sub_141045D50(a1, a2, a3) != 0 )
    return 1;
  v6 = *(_QWORD *)(a1 + 264);
  if ( v6 != 0 && (unsigned __int8)sub_141063F30(v6, v4, a3) != 0 )
    return 1;
  else
    return sub_140FE2700((_DWORD *)a1, v4, a3);
}
