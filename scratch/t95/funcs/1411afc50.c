// THUNK ALIAS -> sub_143FF40B0 (jmp:0x1411afc50->0x143ff40b0)
__int64 __fastcall sub_143FF40B0(__int64 a1)
{
  __int64 v2; // rdi
  bool v3; // zf
  __int64 result; // rax

  if ( byte_141B595A8 != 0 )
  {
    v2 = qword_141B595B0;
    v3 = v2 == (unsigned int)MEMORY[0x141947498](a1);
  }
  else
  {
    v3 = qword_141B5A658 == (unsigned int)MEMORY[0x141947498](a1);
  }
  result = *(_QWORD *)(*(_QWORD *)(a1 + 160) + 184LL);
  if ( v3 && result == 0 )
  {
    *(_QWORD *)(*(_QWORD *)(a1 + 160) + 184LL) = sub_140B530F0(a1);
    return *(_QWORD *)(*(_QWORD *)(a1 + 160) + 184LL);
  }
  return result;
}
