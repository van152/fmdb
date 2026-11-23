__int64 __fastcall sub_140FE8810(unsigned int a1, _QWORD *a2)
{
  __int64 result; // rax
  _QWORD *v4; // rdi

  result = qword_141B60C30;
  if ( qword_141B60C30 == qword_141B60C38 )
    return sub_140835A40(&qword_141B60C30, a1, a2);
  while ( *(_DWORD *)result != a1 )
  {
    result += 16;
    if ( result == qword_141B60C38 )
      return sub_140835A40(&qword_141B60C30, a1, a2);
  }
  if ( result == qword_141B60C38 )
    return sub_140835A40(&qword_141B60C30, a1, a2);
  v4 = *(_QWORD **)(result + 8);
  if ( v4 == nullptr )
    return sub_140835A40(&qword_141B60C30, a1, a2);
  if ( v4 != a2 )
  {
    (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*v4 + 16LL))(*v4, v4);
    return (*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD *))(*(_QWORD *)*a2 + 24LL))(*a2, a2, v4);
  }
  return result;
}
