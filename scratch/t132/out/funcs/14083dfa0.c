__int64 *__fastcall sub_14083DFA0(__int64 *a1, __int64 *a2)
{
  __int64 v4; // rax
  __int64 v5; // rax

  if ( a1 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a1 + 16LL))(a1: *a1, a2: a1);
    v4 = *a2;
    a1[1] = a2[1];
    *a1 = v4;
    v5 = sub_14083D4F0();
    a2[1] = 0;
    *a2 = v5 + 8;
  }
  return a1;
}
