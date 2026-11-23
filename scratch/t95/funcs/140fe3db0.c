// THUNK ALIAS -> sub_143E31DA0 (jmp:0x140fe3db0->0x143e31da0)
__int64 sub_143E31DA0()
{
  __int64 v0; // rcx
  unsigned int v1; // esi
  __int64 *v2; // rax
  __int64 *v3; // rdi

  v0 = qword_141B60C30;
  v1 = 0;
  v2 = nullptr;
  if ( qword_141B60C30 != qword_141B60C38 )
  {
    while ( *(_DWORD *)v0 != 1986359923 )
    {
      v0 += 16;
      if ( v0 == qword_141B60C38 )
        goto LABEL_8;
    }
    if ( v0 == qword_141B60C38 )
      v2 = nullptr;
    else
      v2 = *(__int64 **)(v0 + 8);
  }
LABEL_8:
  v3 = &qword_141B5A4A0;
  if ( v2 != nullptr )
    v3 = v2;
  if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v3 + 8LL))(*v3, v3) != 0 )
    return (*(unsigned int (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v3 + 64LL))(*v3, v3);
  return v1;
}
