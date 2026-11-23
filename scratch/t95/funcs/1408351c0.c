__int64 __fastcall sub_1408351C0(__int64 *a1, __int64 a2, _QWORD *a3)
{
  __int64 result; // rax
  __int64 v5; // rdi
  _QWORD *v6; // rdi

  result = *a1;
  v5 = a1[1];
  if ( *a1 == v5 )
    return sub_140835A40(a1, a2, a3);
  while ( *(_DWORD *)result != (_DWORD)a2 )
  {
    result += 16;
    if ( result == v5 )
      return sub_140835A40(a1, a2, a3);
  }
  if ( result == v5 )
    return sub_140835A40(a1, a2, a3);
  v6 = *(_QWORD **)(result + 8);
  if ( v6 == nullptr )
    return sub_140835A40(a1, a2, a3);
  if ( v6 != a3 )
  {
    (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*v6 + 16LL))(*v6, v6);
    return (*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD *))(*(_QWORD *)*a3 + 24LL))(*a3, a3, v6);
  }
  return result;
}
